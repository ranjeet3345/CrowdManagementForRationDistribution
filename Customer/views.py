from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm, StaffProfileForm, CustomerProfileForm
from django.http import HttpResponseForbidden
from .models import CustomerProfile, StaffProfile,Token,CustomUser
from django.contrib import messages
from .models import CustomerProfile, StaffProfile
from django.db.models import Q

@login_required
def book_token(request, staff_id):
    if request.user.role != 'customer':
        messages.error(request, "Only customers can book tokens.")
        return redirect('home')

    staff = get_object_or_404(CustomUser, id=staff_id)

   
    existing = Token.objects.filter(customer=request.user, is_active=True).first()
    if existing:
        messages.warning(request, "You already have a booked token.")
        return redirect('home')

    
    last_token = Token.objects.filter(staff=staff).order_by('-token_number').first()
    next_token_num = last_token.token_number + 1 if last_token else 1

  
    token = Token.objects.create(
        customer=request.user,
        staff=staff,
        token_number=next_token_num
    )

  
    customer_profile = CustomerProfile.objects.filter(user=request.user).first()
    staff_profile = StaffProfile.objects.filter(user=staff).first()
    staff_profile.noOfTokenBooked=staff_profile.noOfTokenBooked+1
    staff_profile.save()
    

    return render(request, 'Customer/BookedToken.html', {
        'token': token,
        'customer': request.user,
        'staff': staff,
        'customer_profile': customer_profile,
        'staff_profile': staff_profile,
    })




@login_required
def allStaffView(request):
    staffs=StaffProfile.objects.select_related('user')
    
    return render(request,'Customer/allStaffList.html',locals())


@login_required
def allCustomerView(request):
    customers = CustomerProfile.objects.select_related('user')
    return render(request, 'Customer/allCustomerList.html', {'customers': customers})




def signup_view(request):
    if request.method == 'POST':
        print("POST request received for signup form")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            print("Creating profile for the user")
            print("Username:", user.username)
            print("Role:", user.role)

            if user.role == 'staff':
                return redirect('staff_complete_profile')  
            elif user.role == 'customer':
                return redirect('customer_complete_profile')  

            return redirect('home')
    else:
        print("GET request received for signup form")
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})



def home(request):
    print("Logged in user:", request.user.username)
    return render(request, 'Customer/home.html')



@login_required
def editStaffProfile(request):
    if request.method == 'POST':
        print("POST request received for staff profile")
        form = StaffProfileForm(request.POST, request.FILES)
        if form.is_valid():
            staff_profile = form.save(commit=False)  
            staff_profile.user = request.user         
            staff_profile.save()                     
            return redirect('home')
    else:
        print("GET request received for staff profile")
        form = StaffProfileForm()

    return render(request, 'Customer/staffProfileForm.html', {'form': form})


@login_required
def editCustomerProfile(request):
    if request.method == 'POST':
        print("POST request received for customer profile")
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            customer_profile = form.save(commit=False)  
            customer_profile.user = request.user         
            customer_profile.save()                     
            return redirect('home')
    else:
        print("GET request received for customer profile")
        form = CustomerProfileForm()

    return render(request, 'Customer/customerProfileForm.html', {'form': form})





@login_required
def view_profile(request):
    user = request.user

    if user.role == 'customer':
        try:
            profile = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            return redirect('customer_complete_profile')
        return render(request, 'Customer/customerProfile.html', {'profile': profile})

    elif user.role == 'staff':
        try:
            profile = StaffProfile.objects.get(user=user)
        except StaffProfile.DoesNotExist:
            return redirect('staff_complete_profile')
        return render(request, 'Customer/staffProfile.html', {'profile': profile})

    return HttpResponseForbidden("Invalid role.")



@login_required
def showStaffDashBoard(request, staff_id):
    user = get_object_or_404(CustomUser, id=staff_id)
    staff_profile = get_object_or_404(StaffProfile, user=user)

    tokenActive = Token.objects.filter(is_active=True, staff=user, is_used=False, in_queue=False)
    tokenInQueue = Token.objects.filter(is_active=True, staff=user, is_used=False, in_queue=True)
    tokenUsed = Token.objects.filter(is_active=True, staff=user, is_used=True)

    return render(request, 'Customer/showStaffDashboard.html', {
        'staff': user,
        'staff_profile': staff_profile,
        'tokenActive': tokenActive,
        'tokenInQueue': tokenInQueue,
        'tokenUsed': tokenUsed,
    })



@login_required
def customerInQueue(request,token_id):
    token=Token.objects.get(id=token_id)
    token.in_queue=True
    token.save() 
    user_staff=token.staff
    staff_profile=get_object_or_404(StaffProfile, user=user_staff)
    tokenActive = Token.objects.filter(is_active=True, staff=user_staff, is_used=False, in_queue=False)
    tokenInQueue = Token.objects.filter(is_active=True, staff=user_staff, is_used=False, in_queue=True)
    tokenUsed = Token.objects.filter(is_active=True, staff=user_staff, is_used=True)

    return render(request, 'Customer/showStaffDashboard1.html', {
        'staff': user_staff,
        'staff_profile': staff_profile,
        'tokenActive': tokenActive,
        'tokenInQueue': tokenInQueue,
        'tokenUsed': tokenUsed,
    })

@login_required
def haveTakenRation(request,token_id):
    token=Token.objects.get(id=token_id)
    token.is_used=True
    token.save()
    user_staff=token.staff
    staff_profile=get_object_or_404(StaffProfile, user=user_staff)
    tokenActive = Token.objects.filter(is_active=True, staff=user_staff, is_used=False, in_queue=False)
    tokenInQueue = Token.objects.filter(is_active=True, staff=user_staff, is_used=False, in_queue=True)
    tokenUsed = Token.objects.filter(is_active=True, staff=user_staff, is_used=True)

    return render(request, 'Customer/showStaffDashboard2.html', {
        'staff': user_staff,
        'staff_profile': staff_profile,
        'tokenActive': tokenActive,
        'tokenInQueue': tokenInQueue,
        'tokenUsed': tokenUsed,
    })




