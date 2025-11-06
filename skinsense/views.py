from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required


# === HOME PAGE ===
def index(request):
    return render(request, 'skinsense/index.html')


# === ABOUT PAGE ===
def about_page(request):
    return render(request, 'skinsense/about.html')


# === LOGIN PAGE ===
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('skinsense:dashboard_page')  # ✅ important: use namespace
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('skinsense:login')
    return render(request, 'skinsense/login.html')

# === REGISTER PAGE ===
def register_page(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        User = get_user_model()

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('skinsense:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('skinsense:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('skinsense:register')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.is_active = True
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('skinsense:login')

    return render(request, 'skinsense/register.html')


# === DASHBOARD PAGE ===
@login_required(login_url='skinsense:login')
def dashboard_page(request):
    return render(request, 'skinsense/dashboard.html')


# === FOLLOW-UP PAGE ===
@login_required(login_url='skinsense:login')
def followup_page(request):
    return render(request, 'skinsense/followup.html')


# === LOGOUT ===
def logout_user(request):
    django_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('skinsense:login')
