from django.db import models
from django.contrib.auth.models import User
from cardealer.models import CarDealer,Vehicles

# Create your models here.
class tblcontactus(models.Model):
    fullname = models.CharField(max_length=50)
    email= models.EmailField()
    subject=models.CharField(max_length=20)
    message=models.CharField(max_length=200)

    class Meta:
        db_table='tblcontactus'
        verbose_name = 'Contact Us'

    def __str__(self):
        return self.fullname

class tblcustomersignup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.BigIntegerField()

    class Meta:
        db_table='tblcustomersignup'
        verbose_name = 'Customer'

    def __str__(self):
        return str(self.user)

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.PROTECT)
    days = models.CharField(max_length = 3)
    is_complete = models.BooleanField(default = False)