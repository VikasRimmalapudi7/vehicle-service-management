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


class MechanicSalaryForm(forms.Form):
    salary = forms.IntegerField()


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
    cost = forms.IntegerField()
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


# -------------------- Updated Mechanic Status Form -----------------------

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


# -------------------- Feedback and Other Forms -----------------------

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['by', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }


presence_choices = (('Present', 'Present'), ('Absent', 'Absent'))


class AttendanceForm(forms.Form):
    present_status = forms.ChoiceField(choices=presence_choices)
    date = forms.DateField()


class AskDateForm(forms.Form):
    date = forms.DateField()


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 30})
    )
