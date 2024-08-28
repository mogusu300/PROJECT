from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

# View for User Signup
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# View for User Login
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('staff_dashboard')
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# View for User Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# View for User Dashboard (accessible only to regular users)
@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')
    return render(request, 'dashboard.html')

# Custom decorator to check if the user is a staff member
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_active and u.is_staff, login_url=login_url)

# View for Staff Dashboard (accessible only to staff members)
@login_required
@staff_required(login_url='login')
def staff_dashboard(request):
    # Add any context or data needed for the staff dashboard
    context = {}
    return render(request, 'registration/staff_dashboard.html', context)
