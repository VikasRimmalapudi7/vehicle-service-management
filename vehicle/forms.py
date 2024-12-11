from django import forms
from django.contrib.auth.models import User
from . import models

# -------------------- Existing Forms -----------------------

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['address', 'mobile', 'profile_pic']

class MechanicUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class MechanicForm(forms.ModelForm):
    class Meta:
        model = models.Mechanic
        fields = ['address', 'mobile', 'profile_pic', 'skill']

class RequestForm(forms.ModelForm):
    class Meta:
        model = models.Request
        fields = [
            'category', 'vehicle_no', 'vehicle_name', 'vehicle_model', 
            'vehicle_brand', 'problem_description', 'address'
        ]
        widgets = {
            'problem_description': forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }

class AdminRequestForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=models.Customer.objects.all(),
        empty_label="Customer Name",
        to_field_name='id'
    )
    mechanic = forms.ModelChoiceField(
        queryset=models.Mechanic.objects.all(),
        empty_label="Mechanic Name",
        to_field_name='id'
    )
    cost = forms.IntegerField()

class AdminApproveRequestForm(forms.Form):
    mechanic = forms.ModelChoiceField(
        queryset=models.Mechanic.objects.all(),
        empty_label="Mechanic Name",
        to_field_name='id'
    )
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Repairing', 'Repairing'),
        ('Repairing Done', 'Repairing Done'),
        ('Released', 'Released')
    )
    status = forms.ChoiceField(choices=stat)

class UpdateCostForm(forms.Form):
    cost = forms.IntegerField()

class MechanicUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = models.Request
        fields = ['status']
        widgets = {
            'status': forms.Select(
                choices=models.Request.stat,
                attrs={'class': 'form-control'}
            )
        }

class SubscriptionForm(forms.Form):
    PLAN_CHOICES = [
        ('1', '1 Month - $120'),
        ('3', '3 Months - $300'),
        ('12', '12 Months - $1000'),
    ]
    name = forms.CharField(max_length=100, label="Cardholder Name")
    card_number = forms.CharField(max_length=16, label="Card Number")
    expiry_date = forms.DateField(label="Expiry Date", widget=forms.TextInput(attrs={'type': 'date'}))
    cvv = forms.CharField(max_length=3, label="CVV", widget=forms.PasswordInput())
    plan = forms.ChoiceField(choices=PLAN_CHOICES, label="Subscription Plan")

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['by', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }
