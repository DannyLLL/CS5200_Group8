from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_view, name='test_view'),
    path('', views.vehicle_list, name='vehicle_list'),  # Default homepage showing vehicle list
    path('testmysql/', views.testmysql, name='testmysql'),  # Test database connection
    path('reserve/<int:vehicle_id>/', views.reserve_vehicle, name='reserve_vehicle'),  # Reserve a vehicle
    path('reservations/<int:renter_id>/', views.reservation_list, name='reservation_list'),  # List renter's reservations
]
