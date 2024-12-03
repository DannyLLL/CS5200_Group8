from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Vehicles, Reservations, UserProfile, VehicleFeatures
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@login_required
def profile_view(request):
    # Get or create UserProfile for the logged-in user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Extract the fields manually from the request.POST dictionary
        user_profile.first_name = request.POST.get('first_name', user_profile.first_name)
        user_profile.last_name = request.POST.get('last_name', user_profile.last_name)
        user_profile.phone_number = request.POST.get('phone_number', user_profile.phone_number)
        user_profile.address = request.POST.get('address', user_profile.address)

        # Save the updated profile
        user_profile.save()

        # Show success message
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('homepage')

    # Prepare the profile data with default values for None fields
    context = {
        'first_name': user_profile.first_name or '',  # Provide empty string if None
        'last_name': user_profile.last_name or '',
        'phone_number': user_profile.phone_number or '',
        'address': user_profile.address or '',
    }

    return render(request, 'dbapp/profile.html', context)

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def add_vehicle(request):
    if request.method == 'POST':
        # Get form data
        vehicle = Vehicles.objects.create(
            ownerid_id=request.POST['owner_id'],
            make=request.POST['make'],
            model=request.POST['model'],
            year=request.POST['year'],
            dailyrate=request.POST['dailyrate'],
            location=request.POST['location'],
            isavailable=True
        )
        return redirect('list_page')
    return render(request, 'dbapp/add_vehicle.html')

@user_passes_test(is_admin)
def delete_vehicle(request, vehicle_id):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicles, vehicleid=vehicle_id)
        vehicle.delete()
    return redirect('list_page')



def list_page(request):
    vehicles = Vehicles.objects.all()
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        vehicles = vehicles.filter(
            Q(make__icontains=search_query) |
            Q(model__icontains=search_query)
        )

    # Make filter
    make = request.GET.get('make')
    if make:
        vehicles = vehicles.filter(make=make)

    # Location filter
    location = request.GET.get('location')
    if location:
        vehicles = vehicles.filter(location=location)

    # Price filter
    max_price = request.GET.get('max_price')
    if max_price:
        vehicles = vehicles.filter(dailyrate__lte=max_price)

    # Features filter
    features = request.GET.getlist('features')
    if features:
        vehicles = vehicles.filter(vehiclefeatures__featurename__in=features).distinct()

    return render(request, 'dbapp/list_page.html', {
        'vehicles': vehicles,
    })


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()
            # Create a UserProfile linked to the new user
            UserProfile.objects.create(user=user, dateregistered=timezone.now())
            # Log in the user
            login(request, user)
            # Show success message
            messages.success(request, "Account created successfully! You are now logged in.")
            # Redirect to the homepage
            return redirect('profile')
        else:
            # Add error message if the form is not valid
            messages.error(request, "There was an error in your form. Please check the highlighted fields.")
            # The errors will be automatically passed to the form context
    else:
        form = UserCreationForm()
    return render(request, 'dbapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'dbapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'dbapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

def homepage(request):
    return render(request, 'dbapp/homepage.html')

def test_view(request):
    return render(request, 'vehicle_list.html')

def vehicle_list(request):
    vehicles = Vehicles.objects.filter(isavailable=True).order_by('-year')
    paginator = Paginator(vehicles, 9)  # Show 9 vehicles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dbapp/vehicle_list.html', {'vehicles': page_obj})

def testmysql(request):
    """
    A simple view to verify database connection and test the application.
    """
    return render(request, 'dbapp/testmysql.html', {'message': 'Hello, Django!'})

def reserve_vehicle(request, vehicle_id):
    """
    View for reserving a vehicle.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    vehicle = get_object_or_404(Vehicles, vehicleid=vehicle_id)
    # Fetch existing reservations for this vehicle
    reservations = Reservations.objects.filter(vehicleid=vehicle).order_by('startdate')

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # Check for overlapping reservations
        overlapping_reservations = reservations.filter(
            Q(startdate__lte=end_date, enddate__gte=start_date)
        )
        if overlapping_reservations.exists():
            return render(request, 'dbapp/reserve_vehicle.html', {
                'vehicle': vehicle,
                'reservations': reservations,
                'error': 'This vehicle is not available for the selected dates.'
            })

        # Create the reservation
        Reservations.objects.create(
            vehicleid=vehicle,
            renterid=request.user,
            startdate=start_date,
            enddate=end_date,
            reservationstatus='Pending'  #  default status
        )


        
        return redirect('list_page') 

    return render(request, 'dbapp/reserve_vehicle.html', {'vehicle': vehicle, 'reservations': reservations})



@login_required
def reservation_list(request):
    reservations = Reservations.objects.filter(renterid=request.user).select_related('vehicleid')
    return render(request, 'dbapp/reservation_list.html', {'reservations': reservations})

# Listing car for rent
def list_car(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    if request.method == 'POST':
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        price = request.POST['price']
        location = request.POST['location']
        image = request.FILES.get('image')
        
        # Save the car information, setting the owner to the currently logged-in user
        Vehicles.objects.create(
            make=make,
            model=model,
            year=year,
            dailyrate=price,
            location=location,
            isavailable=1,  # Set car availability to true
            ownerid=request.user,  # Set the owner to the currently logged-in user
            image=image
        )
        
        return redirect('manage_car')  # Redirect to the vehicle list page after listing
    
    return render(request, 'dbapp/listing_rental_car.html')

def manage_car(request):
    """
    View to display the car management page.
    """
    if not request.user.is_authenticated:
        # Redirect to login if the user is not authenticated
        return redirect('login')  
    
    # Fetch all cars (or filter based on user if necessary)
    cars = Vehicles.objects.filter(ownerid=request.user)

    # Render the template and pass the list of cars as context
    return render(request, 'dbapp/manage_car.html', {'list_page': cars})
