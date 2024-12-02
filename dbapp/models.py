from django.db import models
from django.contrib.auth.models import User


class CarDelivery(models.Model):
    deliveryid = models.AutoField(db_column='DeliveryID', primary_key=True)
    vehicleid = models.ForeignKey('Vehicles', on_delete=models.CASCADE, db_column='VehicleID', blank=True, null=True)  # Make nullable
    deliveryavailable = models.IntegerField(db_column='DeliveryAvailable', blank=True, null=True)
    deliveryfee = models.DecimalField(db_column='DeliveryFee', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Car_Delivery'


class Notifications(models.Model):
    notificationid = models.AutoField(db_column='NotificationID', primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='UserID', blank=True, null=True)  # Make nullable
    message = models.TextField(db_column='Message')
    isread = models.IntegerField(db_column='IsRead', blank=True, null=True)
    createdat = models.DateTimeField(db_column='CreatedAt')

    class Meta:
        db_table = 'Notifications'


class Payments(models.Model):
    paymentid = models.AutoField(db_column='PaymentID', primary_key=True)
    reservationid = models.ForeignKey('Reservations', on_delete=models.CASCADE, db_column='ReservationID', blank=True, null=True)  # Make nullable
    paymentdate = models.DateTimeField(db_column='PaymentDate')
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)
    paymentstatus = models.CharField(db_column='PaymentStatus', max_length=9, blank=True, null=True)

    class Meta:
        db_table = 'Payments'


class Reservations(models.Model):
    reservationid = models.AutoField(db_column='ReservationID', primary_key=True)
    vehicleid = models.ForeignKey('Vehicles', on_delete=models.CASCADE, db_column='VehicleID', blank=True, null=True)  # Make nullable
    renterid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='RenterID', blank=True, null=True)  # Make nullable
    startdate = models.DateField(db_column='StartDate')
    enddate = models.DateField(db_column='EndDate')
    reservationstatus = models.CharField(db_column='ReservationStatus', max_length=9, blank=True, null=True)

    class Meta:
        db_table = 'Reservations'


class Reviews(models.Model):
    reviewid = models.AutoField(db_column='ReviewID', primary_key=True)
    reviewerid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='ReviewerID', blank=True, null=True)  # Make nullable
    targetid = models.IntegerField(db_column='TargetID')
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)
    reviewtext = models.TextField(db_column='ReviewText', blank=True, null=True)
    reviewtype = models.CharField(db_column='ReviewType', max_length=7)

    class Meta:
        db_table = 'Reviews'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    dateregistered = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'UserProfile'


class VehicleFeatures(models.Model):
    featureid = models.AutoField(db_column='FeatureID', primary_key=True)
    vehicleid = models.ForeignKey('Vehicles', on_delete=models.CASCADE, db_column='VehicleID', blank=True, null=True)  # Make nullable
    featurename = models.CharField(db_column='FeatureName', max_length=50)
    featurevalue = models.CharField(db_column='FeatureValue', max_length=50)

    class Meta:
        db_table = 'Vehicle_Features'


class Vehicles(models.Model):
    vehicleid = models.AutoField(db_column='VehicleID', primary_key=True)
    ownerid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='OwnerID', blank=True, null=True)  # Make nullable
    make = models.CharField(db_column='Make', max_length=50)
    model = models.CharField(db_column='Model', max_length=50)
    year = models.IntegerField(db_column='Year')
    dailyrate = models.DecimalField(db_column='DailyRate', max_digits=10, decimal_places=2)
    location = models.CharField(db_column='Location', max_length=100)
    isavailable = models.IntegerField(db_column='IsAvailable', blank=True, null=True)

    class Meta:
        db_table = 'Vehicles'
