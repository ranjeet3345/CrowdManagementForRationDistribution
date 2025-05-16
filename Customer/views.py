from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # ✅ Make sure this import exists

def home(request):
    print(request)
    return render(request, 'Customer/home.html')