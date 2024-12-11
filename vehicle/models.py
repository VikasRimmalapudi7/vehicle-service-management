from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/CustomerProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"

class Mechanic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/MechanicProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=False)
    skill = models.CharField(max_length=500, null=True)
    status = models.BooleanField(default=False)  # No auto-approval
    premium = models.BooleanField(default=False)
    subscription_plan = models.CharField(
        max_length=20, 
        choices=[('1', '1 Month'), ('3', '3 Months'), ('12', '1 Year')], 
        null=True, 
        blank=True
    )
    subscription_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"


class Request(models.Model):
    cat = (('two wheeler with gear', 'two wheeler with gear'), ('two wheeler without gear', 'two wheeler without gear'),
           ('three wheeler', 'three wheeler'), ('four wheeler', 'four wheeler'))
    category = models.CharField(max_length=50, choices=cat)
    vehicle_no = models.PositiveIntegerField(null=False)
    vehicle_name = models.CharField(max_length=40, null=False)
    vehicle_model = models.CharField(max_length=40, null=False)
    vehicle_brand = models.CharField(max_length=40, null=False)
    problem_description = models.CharField(max_length=500, null=False)
    date = models.DateField(auto_now=True)
    cost = models.PositiveIntegerField(null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE, null=True)
    stat = (('Approved', 'Approved'), ('Repairing', 'Repairing'), 
            ('Repairing Done', 'Repairing Done'))
    status = models.CharField(max_length=50, choices=stat, default='Pending', null=True)
    address = models.CharField(max_length=100, null=True, blank=True)  

class Feedback(models.Model):
    date = models.DateField(auto_now=True)
    by = models.CharField(max_length=40)
    message = models.CharField(max_length=500)
