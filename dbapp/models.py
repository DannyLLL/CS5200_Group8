# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CarDelivery(models.Model):
    deliveryid = models.AutoField(db_column='DeliveryID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey('Vehicles', models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    deliveryavailable = models.IntegerField(db_column='DeliveryAvailable', blank=True, null=True)  # Field name made lowercase.
    deliveryfee = models.DecimalField(db_column='DeliveryFee', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Car_Delivery'


class Notifications(models.Model):
    notificationid = models.AutoField(db_column='NotificationID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    message = models.TextField(db_column='Message')  # Field name made lowercase.
    isread = models.IntegerField(db_column='IsRead', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt')  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Notifications'


class Payments(models.Model):
    paymentid = models.AutoField(db_column='PaymentID', primary_key=True)  # Field name made lowercase.
    reservationid = models.ForeignKey('Reservations', models.DO_NOTHING, db_column='ReservationID')  # Field name made lowercase.
    paymentdate = models.DateTimeField(db_column='PaymentDate')  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentstatus = models.CharField(db_column='PaymentStatus', max_length=9, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Payments'


class Reservations(models.Model):
    reservationid = models.AutoField(db_column='ReservationID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey('Vehicles', models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    renterid = models.ForeignKey('Users', models.DO_NOTHING, db_column='RenterID')  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate')  # Field name made lowercase.
    reservationstatus = models.CharField(db_column='ReservationStatus', max_length=9, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Reservations'


class Reviews(models.Model):
    reviewid = models.AutoField(db_column='ReviewID', primary_key=True)  # Field name made lowercase.
    reviewerid = models.ForeignKey('Users', models.DO_NOTHING, db_column='ReviewerID')  # Field name made lowercase.
    targetid = models.IntegerField(db_column='TargetID')  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    reviewtext = models.TextField(db_column='ReviewText', blank=True, null=True)  # Field name made lowercase.
    reviewtype = models.CharField(db_column='ReviewType', max_length=7)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Reviews'


class Users(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='PasswordHash', max_length=255)  # Field name made lowercase.
    usertype = models.CharField(db_column='UserType', max_length=6)  # Field name made lowercase.
    dateregistered = models.DateTimeField(db_column='DateRegistered')  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Users'


class VehicleFeatures(models.Model):
    featureid = models.AutoField(db_column='FeatureID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey('Vehicles', models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    featurename = models.CharField(db_column='FeatureName', max_length=50)  # Field name made lowercase.
    featurevalue = models.CharField(db_column='FeatureValue', max_length=50)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Vehicle_Features'


class Vehicles(models.Model):
    vehicleid = models.AutoField(db_column='VehicleID', primary_key=True)  # Field name made lowercase.
    ownerid = models.ForeignKey(Users, models.DO_NOTHING, db_column='OwnerID')  # Field name made lowercase.
    make = models.CharField(db_column='Make', max_length=50)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=50)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    dailyrate = models.DecimalField(db_column='DailyRate', max_digits=10, decimal_places=2)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=100)  # Field name made lowercase.
    isavailable = models.IntegerField(db_column='IsAvailable', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Vehicles'
