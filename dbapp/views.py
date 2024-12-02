from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.db import connection 
from django.urls import reverse_lazy
from .models import Vehicles, Reservations
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vehicles, Reservations, Users
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages




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
    vehicles = Vehicles.objects.filter(isavailable=True)
    return render(request, 'dbapp/list_page.html', {'vehicles': vehicles})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            # Add error message handling here
            return render(request, 'dbapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'dbapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        
        if password != password2:
            return render(request, 'dbapp/register.html', {'error': 'Passwords do not match'})
            
        # Create user in your Users table
        user = Users.objects.create(
            username=username,
            email=email,
            passwordhash=password,  # In production, you should hash this password
            usertype='Renter',
            dateregistered=timezone.now()
        )
        
        return redirect('login')
    return render(request, 'dbapp/register.html')



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


# Vehicle Reservation View
def reserve_vehicle(request, vehicle_id):
    """
    Placeholder View for reserving a vehicle.
    This will allow users to reserve a specific vehicle once migrations are complete.
    """
    vehicle = get_object_or_404(Vehicles, pk=vehicle_id)  # This line will only work after migrations

    if request.method == 'POST':
        # Create a reservation (will only work after migrations)
        Reservations.objects.create(
            vehicleid=vehicle,
            renterid_id=request.POST['renter_id'],
            startdate=request.POST['start_date'],
            enddate=request.POST['end_date'],
            reservationstatus='Pending'
        )
        # Update vehicle availability
        vehicle.isavailable = False
        vehicle.save()
        return render(request, 'success.html', {'vehicle': vehicle})

    return render(request, 'reserve_vehicle.html', {'vehicle': vehicle})

# Optional Reservation List View
def reservation_list(request, renter_id):
    """
    Placeholder View for listing all reservations for a specific renter.
    """
    reservations = Reservations.objects.filter(renterid_id=renter_id)
    return render(request, 'reservation_list.html', {'reservations': reservations})
