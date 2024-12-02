# dbapp/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Vehicles,
    Reservations,
    Payments,
    Reviews,
    CarDelivery,
    VehicleFeatures,
    Notifications
)

@admin.register(Reservations)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservationid', 'vehicle_info', 'renter_info', 'date_range', 
                   'reservationstatus', 'payment_status')
    list_filter = ('reservationstatus', 'startdate', 'enddate')
    search_fields = ('renterid__username', 'vehicleid__make', 'vehicleid__model')
    list_per_page = 20

    def vehicle_info(self, obj):
        return format_html(
            '<div><strong>{} {} {}</strong><br>Location: {}</div>',
            obj.vehicleid.year,
            obj.vehicleid.make,
            obj.vehicleid.model,
            obj.vehicleid.location
        )
    vehicle_info.short_description = 'Vehicle'

    def renter_info(self, obj):
        return format_html(
            '<div><strong>{}</strong><br>{}</div>',
            obj.renterid.username,
            obj.renterid.email
        )
    renter_info.short_description = 'Renter'

    def date_range(self, obj):
        return format_html(
            '<div>From: {}<br>To: {}</div>',
            obj.startdate,
            obj.enddate
        )
    date_range.short_description = 'Rental Period'

    def payment_status(self, obj):
        payment = Payments.objects.filter(reservationid=obj).first()
        if payment:
            color = 'green' if payment.paymentstatus == 'Completed' else 'red'
            return format_html(
                '<span style="color: {};">{}</span>',
                color,
                payment.paymentstatus
            )
        return format_html('<span style="color: gray;">No Payment</span>')
    payment_status.short_description = 'Payment Status'

@admin.register(Vehicles)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicleid', 'owner_info', 'vehicle_details', 'dailyrate', 
                   'location', 'availability_status', 'delivery_option')
    list_filter = ('isavailable', 'location', 'make', 'year')
    search_fields = ('make', 'model', 'ownerid__username')
    list_editable = ('dailyrate',)

    def owner_info(self, obj):
        return format_html(
            '<div><strong>{}</strong><br>{}</div>',
            obj.ownerid.username,
            obj.ownerid.email
        )
    owner_info.short_description = 'Owner'

    def vehicle_details(self, obj):
        return f"{obj.year} {obj.make} {obj.model}"
    vehicle_details.short_description = 'Vehicle'

    def availability_status(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.isavailable else 'red',
            'Available' if obj.isavailable else 'Not Available'
        )
    availability_status.short_description = 'Status'

    def delivery_option(self, obj):
        delivery = CarDelivery.objects.filter(vehicleid=obj).first()
        if delivery and delivery.deliveryavailable:
            return format_html(
                'Yes (${:.2f})',
                delivery.deliveryfee
            )
        return 'No'
    delivery_option.short_description = 'Delivery'

@admin.register(Payments)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('paymentid', 'reservation_info', 'amount', 'paymentstatus', 'paymentdate')
    list_filter = ('paymentstatus', 'paymentdate')
    search_fields = ('reservationid__renterid__username',)

    def reservation_info(self, obj):
        return format_html(
            '<div>ID: {}<br>Renter: {}</div>',
            obj.reservationid.reservationid,
            obj.reservationid.renterid.username
        )
    reservation_info.short_description = 'Reservation'

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewid', 'reviewerid', 'rating', 'reviewtype', 'review_preview')
    list_filter = ('reviewtype', 'rating')
    search_fields = ('reviewerid__username', 'reviewtext')

    def review_preview(self, obj):
        return obj.reviewtext[:100] + '...' if obj.reviewtext else ''
    review_preview.short_description = 'Review'

# Register remaining models
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'usertype', 'dateregistered')

admin.site.register(CarDelivery)
admin.site.register(VehicleFeatures)
admin.site.register(Notifications)
