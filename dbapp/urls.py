from django.urls import path
from . import views

urlpatterns = [

    path('', views.homepage, name='homepage'),  # Homepage
    # path('rent/', views.vehicle_list, name='vehicle_list'),  # Rent vehicles (vehicle list)
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('list/', views.list_page, name='list_page'),  # Listing page

    #path('', views.vehicle_list, name='vehicle_list'),  # Default homepage showing vehicle list

    path('reserve/<int:vehicle_id>/', views.reserve_vehicle, name='reserve_vehicle'),  # Reserve a vehicle
    path('reservations/<int:renter_id>/', views.reservation_list, name='reservation_list'),  # List renter's reservations
    path('testmysql/', views.testmysql, name='testmysql'),  # Test database connection

    path('login/', views.login_view, name='login'), #login page
    path('logout/', views.logout_view, name='logout'), #logout page
    path('register/', views.register_view, name='register'), #register page
    path('list/', views.list_page, name='list_page'), #list page
    path('vehicle/add/', views.add_vehicle, name='add_vehicle'), #add vehicle
    path('vehicle/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'), #delete vehicle
]
