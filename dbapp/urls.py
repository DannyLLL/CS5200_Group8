from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.homepage, name='homepage'),  # Homepage
    # path('rent/', views.vehicle_list, name='vehicle_list'),  # Rent vehicles (vehicle list)
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('list/', views.list_page, name='list_page'),  # Listing page

    #path('', views.vehicle_list, name='vehicle_list'),  # Default homepage showing vehicle list

    path('reserve/<int:vehicle_id>/', views.reserve_vehicle, name='reserve_vehicle'),  # Reserve a vehicle
    path('reservations/', views.reservation_list, name='reservation_list'), # List renter's reservations
    path('reservation/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('payment/<int:reservation_id>/', views.payment, name='payment'),
    path('testmysql/', views.testmysql, name='testmysql'),  # Test database connection


    path('login/', views.login_view, name='login'), #login page
    path('logout/', views.logout_view, name='logout'), #logout page
    path('register/', views.register_view, name='register'), #register page
    path('profile/', views.profile_view, name='profile'),


    path('list/', views.list_page, name='list_page'), #list page
    path('vehicle/add/', views.add_vehicle, name='add_vehicle'), #add vehicle
    path('vehicle/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'), #delete vehicle
    path('list_car/', views.list_car, name='listing_rental_car'),  # Use the correct name
    path('manage_car/', views.manage_car, name='manage_car'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)