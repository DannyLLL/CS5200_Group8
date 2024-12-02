from django.shortcuts import render, get_object_or_404
# Create your views here. 
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


def homepage(request):
    return render(request, 'dbapp/homepage.html')

def test_view(request):
    return render(request, 'vehicle_list.html')

# Listing view
def list_page(request):
    return render(request, 'list_page.html')


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
