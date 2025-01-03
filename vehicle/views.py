from datetime import timezone
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.db.models import Q
from django.db import connection
from django.utils import timezone


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/index.html')


#for showing signup/login button for customer
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/customerclick.html')

#for showing signup/login button for mechanics
def mechanicsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'vehicle/mechanicsclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,'vehicle/customersignup.html',context=mydict)


def mechanic_signup_view(request):
    userForm = forms.MechanicUserForm()
    mechanicForm = forms.MechanicForm()
    mydict = {'userForm': userForm, 'mechanicForm': mechanicForm}
    
    if request.method == 'POST':
        userForm = forms.MechanicUserForm(request.POST)
        mechanicForm = forms.MechanicForm(request.POST, request.FILES)
        
        if userForm.is_valid() and mechanicForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            
            mechanic = mechanicForm.save(commit=False)
            mechanic.user = user
            # No auto-approval
            mechanic.save()
            
            # Assign to MECHANIC group
            my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
            my_mechanic_group[0].user_set.add(user)
            
            return HttpResponseRedirect('mechaniclogin')
    
    return render(request, 'vehicle/mechanicsignup.html', context=mydict)



#for checking user customer, mechanic or admin(by sumit)
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()
def is_mechanic(user):
    return user.groups.filter(name='MECHANIC').exists()


def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-dashboard')
    elif is_mechanic(request.user):
        mechanic = models.Mechanic.objects.filter(user_id=request.user.id).first()
        if mechanic and mechanic.status:  # Only approved mechanics proceed
            return redirect('mechanic-dashboard')
        else:
            return render(request, 'vehicle/mechanic_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')




#============================================================================================
# ADMIN RELATED views start
#============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    dict={
    'total_customer':models.Customer.objects.all().count(),
    'total_mechanic':models.Mechanic.objects.all().count(),
    'total_request':models.Request.objects.all().count(),
    'total_feedback':models.Feedback.objects.all().count(),
    'data':zip(customers,enquiry),
    }
    return render(request,'vehicle/admin_dashboard.html',context=dict)


@login_required(login_url='adminlogin')
def admin_customer_view(request):
    return render(request,'vehicle/admin_customer.html')

@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'vehicle/admin_view_customer.html',{'customers':customers})


@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('admin-view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'vehicle/update_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_add_customer_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-customer')
    return render(request,'vehicle/admin_add_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_customer_enquiry_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'vehicle/admin_view_customer_enquiry.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def admin_view_customer_invoice_view(request):
    enquiry=models.Request.objects.values('customer_id').annotate(Sum('cost'))
    print(enquiry)
    customers=[]
    for enq in enquiry:
        print(enq)
        customer=models.Customer.objects.get(id=enq['customer_id'])
        customers.append(customer)
    return render(request,'vehicle/admin_view_customer_invoice.html',{'data':zip(customers,enquiry)})

@login_required(login_url='adminlogin')
def admin_mechanic_view(request):
    return render(request,'vehicle/admin_mechanic.html')


@login_required(login_url='adminlogin')
def admin_approve_mechanic_view(request):
    mechanics=models.Mechanic.objects.all().filter(status=False)
    return render(request,'vehicle/admin_approve_mechanic.html',{'mechanics':mechanics})

@login_required(login_url='adminlogin')
def approve_mechanic_view(request, pk):
    mechanic = models.Mechanic.objects.get(id=pk)
    if request.method == 'POST':
        mechanic.status = True
        mechanic.save()
        return HttpResponseRedirect('/admin-approve-mechanic')
    return render(request, 'vehicle/admin_approve_mechanic_details.html', {'mechanic': mechanic})


@login_required(login_url='adminlogin')
def delete_mechanic_view(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    user.delete()
    mechanic.delete()
    return redirect('admin-approve-mechanic')


@login_required(login_url='adminlogin')
def admin_add_mechanic_view(request):
    userForm=forms.MechanicUserForm()
    mechanicForm=forms.MechanicForm()
    mydict={'userForm':userForm,'mechanicForm':mechanicForm}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanic=mechanicForm.save(commit=False)
            mechanic.user=user
            mechanic.status=True
            mechanic.save()
            my_mechanic_group = Group.objects.get_or_create(name='MECHANIC')
            my_mechanic_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-mechanic')
        else:
            print('problem in form')
    return render(request,'vehicle/admin_add_mechanic.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_view_mechanic_view(request):
    mechanics = models.Mechanic.objects.all()
    return render(request, 'vehicle/admin_view_mechanic.html', {'mechanics': mechanics})


@login_required(login_url='adminlogin')
def delete_mechanic_view(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    user.delete()
    mechanic.delete()
    return redirect('admin-view-mechanic')


@login_required(login_url='adminlogin')
def update_mechanic_view(request,pk):
    mechanic=models.Mechanic.objects.get(id=pk)
    user=models.User.objects.get(id=mechanic.user_id)
    userForm=forms.MechanicUserForm(instance=user)
    mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
    mydict={'userForm':userForm,'mechanicForm':mechanicForm}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST,instance=user)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('admin-view-mechanic')
    return render(request,'vehicle/update_mechanic.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request,'vehicle/admin_request.html')

@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request,'vehicle/admin_view_request.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request, pk):
    enquiry_x = models.Request.objects.get(id=pk)

    # Prevent changes if status is not pending
    if enquiry_x.status != 'Pending':
        return HttpResponseRedirect('/admin-view-request')

    # Initialize form with existing data
    adminenquiry = forms.AdminApproveRequestForm(initial={
        'mechanic': enquiry_x.mechanic,
        'status': enquiry_x.status,
    })

    if request.method == 'POST':
        adminenquiry = forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x.mechanic = adminenquiry.cleaned_data['mechanic']
            enquiry_x.status = adminenquiry.cleaned_data['status']
            enquiry_x.save()
            return HttpResponseRedirect('/admin-view-request')

    return render(request, 'vehicle/admin_approve_request_details.html', {'adminenquiry': adminenquiry})




@login_required(login_url='adminlogin')
def admin_delete_request_view(request,pk):
    requests=models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')



@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry = forms.RequestForm()
    adminenquiry = forms.AdminRequestForm()
    premium_mechanics = models.Mechanic.objects.filter(premium=True)

    adminenquiry.fields['mechanic'].queryset = premium_mechanics  # Only premium mechanics

    if request.method == 'POST':
        enquiry = forms.RequestForm(request.POST)
        adminenquiry = forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x = enquiry.save(commit=False)
            enquiry_x.customer = adminenquiry.cleaned_data['customer']
            enquiry_x.mechanic = adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost = adminenquiry.cleaned_data['cost']
            enquiry_x.status = 'Approved'
            enquiry_x.save()
        return HttpResponseRedirect('admin-view-request')

    return render(request, 'vehicle/admin_add_request.html', {'enquiry': enquiry, 'adminenquiry': adminenquiry})


@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry=models.Request.objects.all().filter(status='Pending')
    return render(request,'vehicle/admin_approve_request.html',{'enquiry':enquiry})

@login_required(login_url='adminlogin')
def approve_request_view(request,pk):
    adminenquiry=forms.AdminApproveRequestForm()
    if request.method=='POST':
        adminenquiry=forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.mechanic=adminenquiry.cleaned_data['mechanic']
            enquiry_x.cost=adminenquiry.cleaned_data['cost']
            enquiry_x.status=adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request,'vehicle/admin_approve_request_details.html',{'adminenquiry':adminenquiry})




@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry=models.Request.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    print(customers)
    return render(request,'vehicle/admin_view_service_cost.html',{'data':zip(customers,enquiry)})


@login_required(login_url='adminlogin')
def update_cost_view(request,pk):
    updateCostForm=forms.UpdateCostForm()
    if request.method=='POST':
        updateCostForm=forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x=models.Request.objects.get(id=pk)
            enquiry_x.cost=updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request,'vehicle/update_cost.html',{'updateCostForm':updateCostForm})


@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports=models.Request.objects.all().filter(Q(status="Repairing Done") | Q(status="Released"))
    dict={
        'reports':reports,
    }
    return render(request,'vehicle/admin_report.html',context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback=models.Feedback.objects.all().order_by('-id')
    return render(request,'vehicle/admin_feedback.html',{'feedback':feedback})

#============================================================================================
# ADMIN RELATED views END
#============================================================================================


#============================================================================================
# CUSTOMER RELATED views start
#============================================================================================

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_dashboard_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    
    # Existing counts
    work_in_progress = models.Request.objects.filter(customer_id=customer.id, status='Repairing').count()
    work_completed = models.Request.objects.filter(customer_id=customer.id).filter(
        Q(status="Repairing Done") | Q(status="Released")
    ).count()
    new_request_made = models.Request.objects.filter(customer_id=customer.id).filter(
        Q(status="Pending")
    ).count()
    bill = models.Request.objects.filter(customer_id=customer.id).filter(
        Q(status="Repairing Done") | Q(status="Released")
    ).aggregate(Sum('cost'))

    # New logic for "Request Approved"
    request_approved = models.Request.objects.filter(customer_id=customer.id, status='Approved').count()

    # Context for the dashboard
    dict = {
        'work_in_progress': work_in_progress,
        'work_completed': work_completed,
        'new_request_made': new_request_made,
        'bill': bill['cost__sum'],
        'request_approved': request_approved,
        'customer': customer,
    }
    return render(request, 'vehicle/customer_dashboard.html', context=dict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_work_details_view(request, status):
    customer = models.Customer.objects.get(user_id=request.user.id)

    # Fetch works based on status
    works = models.Request.objects.filter(customer_id=customer.id, status=status).select_related('mechanic')

    return render(request, 'vehicle/customer_work_details.html', {
        'works': works,
        'status': status,
    })



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_request.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id , status="Pending")
    return render(request,'vehicle/customer_view_request.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_delete_request_view(request,pk):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_view_approved_request.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_view_approved_request_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_view_approved_request_invoice.html',{'customer':customer,'enquiries':enquiries})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_add_request_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    enquiry = forms.RequestForm()
    if request.method == 'POST':
        enquiry = forms.RequestForm(request.POST)
        if enquiry.is_valid():
            enquiry_x = enquiry.save(commit=False)
            enquiry_x.customer = customer
            enquiry_x.address = customer.address  # Assign customer’s address
            enquiry_x.save()
        else:
            print("Form is invalid")
        return HttpResponseRedirect('customer-dashboard')
    return render(request, 'vehicle/customer_add_request.html', {'enquiry': enquiry, 'customer': customer})



@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_profile.html',{'customer':customer})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_customer_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer-profile')
    return render(request,'vehicle/edit_customer_profile.html',context=mydict)


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_invoice_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiries=models.Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'vehicle/customer_invoice.html',{'customer':customer,'enquiries':enquiries})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_feedback_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent_by_customer.html',{'customer':customer})
    return render(request,'vehicle/customer_feedback.html',{'feedback':feedback,'customer':customer})
#============================================================================================
# CUSTOMER RELATED views END
#============================================================================================






#============================================================================================
# MECHANIC RELATED views start
#============================================================================================


from django.db.models import Sum  # Ensure this is imported

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_dashboard_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    work_in_progress = models.Request.objects.filter(mechanic_id=mechanic.id, status='Repairing').count()
    work_completed = models.Request.objects.filter(mechanic_id=mechanic.id, status='Repairing Done').count()
    new_work_assigned = models.Request.objects.filter(mechanic_id=mechanic.id, status='Approved').count()

    # Calculate total earnings
    total_earnings = models.Request.objects.filter(mechanic_id=mechanic.id, status='Repairing Done').aggregate(
        total=Sum('cost')
    )['total'] or 0

    dict = {
        'work_in_progress': work_in_progress,
        'work_completed': work_completed,
        'new_work_assigned': new_work_assigned,
        'mechanic': mechanic,
        'total_earnings': total_earnings,  # Add total earnings to context
    }
    return render(request, 'vehicle/mechanic_dashboard.html', context=dict)



@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_work_details_view(request, status):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    works = models.Request.objects.filter(mechanic_id=mechanic.id, status=status)
    
    context = {
        'works': works,
        'status': status,
        'mechanic': mechanic,
    }
    return render(request, 'vehicle/mechanic_work_details.html', context)

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_update_status_view(request, pk):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)
    
    try:
        request_obj = models.Request.objects.get(id=pk)
    except models.Request.DoesNotExist:
        return redirect('mechanic-work-assigned')  # Redirect to assigned works

    if request.method == 'POST':
        updateStatus = forms.MechanicUpdateStatusForm(request.POST, instance=request_obj)
        if updateStatus.is_valid():
            # Check if the status is "Repairing Done"
            if updateStatus.cleaned_data['status'] == 'Repairing Done':
                cost = request.POST.get('cost')
                if not cost:
                    # If cost is not provided, reload the form with an error message
                    return render(request, 'vehicle/mechanic_update_status.html', {
                        'updateStatus': updateStatus,
                        'mechanic': mechanic,
                        'error': "Cost is required when marking status as 'Repairing Done'."
                    })
                request_obj.cost = cost  # Assign the cost to the request object
            
            # Assign the mechanic if not already assigned
            if request_obj.mechanic is None:
                request_obj.mechanic = mechanic

            # Save the changes
            updateStatus.save()
            return redirect('mechanic-work-assigned')
        else:
            print("Form errors:", updateStatus.errors)
    
    updateStatus = forms.MechanicUpdateStatusForm(instance=request_obj)
    return render(request, 'vehicle/mechanic_update_status.html', {
        'updateStatus': updateStatus,
        'mechanic': mechanic,
    })




@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_work_assigned_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)

    # Check if the mechanic is premium
    if not mechanic.premium:
        return render(request, 'vehicle/no_access.html')  # Redirect to no access page if not premium

    # Fetch requests assigned to premium mechanics
    works = models.Request.objects.filter(address=mechanic.address,
        mechanic=mechanic
    ).exclude(status__in=['Repairing Done', 'Released'])  # Exclude completed requests

    # You may want to add additional logic if premium mechanics should see all requests
    # Example: If they should also see unassigned requests (those without a mechanic assigned)
    if mechanic.premium:
        works = works | models.Request.objects.filter(address=mechanic.address,mechanic__isnull=True)

    return render(request, 'vehicle/mechanic_work_assigned.html', {
        'works': works,
        'mechanic': mechanic
    })


from datetime import timedelta
from django.utils import timezone

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def subscribe_to_premium_view(request):
    mechanic = models.Mechanic.objects.get(user_id=request.user.id)

    # Subscription Details if Already Subscribed
    if mechanic.premium:
        plan_text = dict(forms.SubscriptionForm.PLAN_CHOICES).get(mechanic.subscription_plan, "Unknown")
        remaining_days = (mechanic.subscription_end_date - timezone.now().date()).days

        context = {
            'mechanic': mechanic,
            'plan_text': plan_text,
            'subscription_date': mechanic.subscription_date,
            'subscription_end_date': mechanic.subscription_end_date,
            'remaining_days': remaining_days
        }

        # Handle renewal
        if request.method == 'POST':
            form = forms.SubscriptionForm(request.POST)
            if form.is_valid():
                selected_plan = form.cleaned_data['plan']
                plan_durations = {'1': 30, '3': 90, '12': 365}

                # Renew subscription
                mechanic.subscription_plan = selected_plan
                mechanic.subscription_date = timezone.now().date()
                mechanic.subscription_end_date += timedelta(days=plan_durations[selected_plan])
                mechanic.save()
                return redirect('mechanic-dashboard')

        context['form'] = forms.SubscriptionForm()
        return render(request, 'vehicle/already_subscribed.html', context)

    # New Subscription
    form = forms.SubscriptionForm()
    if request.method == 'POST':
        form = forms.SubscriptionForm(request.POST)
        if form.is_valid():
            selected_plan = form.cleaned_data['plan']
            plan_durations = {'1': 30, '3': 90, '12': 365}

            # Set Subscription Details
            mechanic.premium = True
            mechanic.subscription_plan = selected_plan
            mechanic.subscription_date = timezone.now().date()
            mechanic.subscription_end_date = mechanic.subscription_date + timedelta(days=plan_durations[selected_plan])
            mechanic.save()
            return redirect('mechanic-dashboard')

    return render(request, 'vehicle/subscribe_to_premium.html', {'form': form})


@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_feedback_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    feedback=forms.FeedbackForm()
    if request.method=='POST':
        feedback=forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request,'vehicle/feedback_sent.html',{'mechanic':mechanic})
    return render(request,'vehicle/mechanic_feedback.html',{'feedback':feedback,'mechanic':mechanic})



@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def mechanic_profile_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    return render(request,'vehicle/mechanic_profile.html',{'mechanic':mechanic})

@login_required(login_url='mechaniclogin')
@user_passes_test(is_mechanic)
def edit_mechanic_profile_view(request):
    mechanic=models.Mechanic.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=mechanic.user_id)
    userForm=forms.MechanicUserForm(instance=user)
    mechanicForm=forms.MechanicForm(request.FILES,instance=mechanic)
    mydict={'userForm':userForm,'mechanicForm':mechanicForm,'mechanic':mechanic}
    if request.method=='POST':
        userForm=forms.MechanicUserForm(request.POST,instance=user)
        mechanicForm=forms.MechanicForm(request.POST,request.FILES,instance=mechanic)
        if userForm.is_valid() and mechanicForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mechanicForm.save()
            return redirect('mechanic-profile')
    return render(request,'vehicle/edit_mechanic_profile.html',context=mydict)






#============================================================================================
# MECHANIC RELATED views start
#============================================================================================




# for aboutus and contact
def aboutus_view(request):
    return render(request,'vehicle/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'vehicle/contactussuccess.html')
    return render(request, 'vehicle/contactus.html', {'form':sub})