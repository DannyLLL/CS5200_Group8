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
from django.contrib.messages import constants as messages_constants



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

def delete_vehicle(request, vehicle_id):
    """
    Delete a vehicle and handle its reservations.
    """
    vehicle = get_object_or_404(Vehicles, vehicleid=vehicle_id)

    if request.method == 'POST':
        # Delete associated reservations
        Reservations.objects.filter(vehicleid=vehicle).delete()
        # Delete the vehicle
        vehicle.delete()
        messages.success(request, 'Vehicle and associated reservations have been deleted.')

        # Redirect based on user type
        if request.user.is_superuser:
            return redirect('list_page')  # Admin redirection
        else:
            return redirect('manage_car')  # Regular user redirection


    return render(request, 'dbapp/confirm_delete_vehicle.html', {'vehicle': vehicle})



def list_page(request):
    vehicles = Vehicles.objects.all()

    # Fetch make
    makes = Vehicles.objects.values_list('make', flat=True).distinct()

    # Fetch locations
    locations = Vehicles.objects.values_list('location', flat=True).distinct()

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

    # Price range filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        vehicles = vehicles.filter(dailyrate__gte=min_price)  # Minimum price filter
    if max_price:
        vehicles = vehicles.filter(dailyrate__lte=max_price)  # Maximum price filter

    # Reservation date filters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        # Exclude vehicles with overlapping reservations
        vehicles = vehicles.exclude(
            reservations__startdate__lt=end_date,
            reservations__enddate__gt=start_date
        )

    # Features filter
    features = request.GET.getlist('features')
    if features:
        vehicles = vehicles.filter(vehiclefeatures__featurename__in=features).distinct()

    return render(request, 'dbapp/list_page.html', {
        'vehicles': vehicles,
        'makes': makes,
        'locations': locations,
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
    vehicles = Vehicles.objects.all()
    locations = Vehicles.objects.values_list('location', flat=True).distinct()

    return render(request, 'dbapp/homepage.html', {
        'vehicles': vehicles,
        'locations': locations,
    })

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

@login_required
def reserve_vehicle(request, vehicle_id):
    """
    View for reserving a vehicle.
    """
    vehicle = get_object_or_404(Vehicles, vehicleid=vehicle_id)

    # check if the current user is the owner
    if vehicle.ownerid == request.user:
        messages.error(request, "You cannot reserve your own car.", extra_tags='no-reserve')
        return redirect('list_page')

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

        # Create reservation with status 'Pending'
        reservation = Reservations.objects.create(
            vehicleid=vehicle,
            renterid=request.user,
            startdate=start_date,
            enddate=end_date,
            reservationstatus='Pending'  # Default status
        )

        # Redirect to payment page
        return redirect('payment', reservation_id=reservation.reservationid)

    return render(request, 'dbapp/reserve_vehicle.html', {'vehicle': vehicle, 'reservations': reservations})



@login_required
def reservation_list(request):
    """
    View for listing all reservations for the logged-in user.
    """
    reservations = Reservations.objects.filter(renterid=request.user).select_related('vehicleid')
    return render(request, 'dbapp/reservation_list.html', {'reservations': reservations})
# Listing car for rent
def list_car(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    if not request.user:
        print("User is None")

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

@login_required
def delete_reservation(request, reservation_id):
    """
    Delete a reservation for the logged-in user.
    """
    reservation = get_object_or_404(Reservations, reservationid=reservation_id, renterid=request.user)

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation has been deleted.')
        return redirect('reservation_list')

    return render(request, 'dbapp/confirm_delete_reservation.html', {'reservation': reservation})

@login_required
def payment(request, reservation_id):
    """
    View for processing payment.
    """
    reservation = get_object_or_404(Reservations, reservationid=reservation_id, renterid=request.user)

    if request.method == 'POST':
        # Simulate payment processing
        credit_card_name = request.POST['credit_card_name']
        credit_card_number = request.POST['credit_card_number']
        exp_date = request.POST['exp_date']
        cvv = request.POST['cvv']
        zip_code = request.POST['zip_code']

        # (For the showcase, assume payment is always successful)
        if credit_card_name and credit_card_number and exp_date and cvv and zip_code:
            # Update reservation status to 'Confirmed'
            reservation.reservationstatus = 'Confirmed'
            reservation.save()

            # Redirect to "My Reservations" page
            messages.success(request, 'Payment successful! Your reservation is confirmed.')
            return redirect('reservation_list')
        else:
            messages.error(request, 'Payment failed. Please check your details and try again.')

    return render(request, 'dbapp/payment.html', {'reservation': reservation})


@login_required
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicles, vehicleid=vehicle_id, ownerid=request.user)

    if request.method == 'POST':
        # Update vehicle details from the form
        vehicle.make = request.POST.get('make', vehicle.make)
        vehicle.model = request.POST.get('model', vehicle.model)
        vehicle.year = request.POST.get('year', vehicle.year)
        vehicle.dailyrate = request.POST.get('dailyrate', vehicle.dailyrate)
        vehicle.location = request.POST.get('location', vehicle.location)
        vehicle.save()

        messages.success(request, 'Vehicle details updated successfully.')
        return redirect('manage_car')  # Redirect back to the car management page

    # Render the edit form with the existing data pre-filled
    return render(request, 'dbapp/edit_vehicle.html', {'vehicle': vehicle})