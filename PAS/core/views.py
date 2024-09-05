from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.validators import validate_email
from .models import CustomUser
from .forms import PassportApplicationForm
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_invalid(self, form):
        # Display a specific error message for email if it's invalid
        if 'email' in form.errors:
            messages.error(self.request, form.errors['email'][0])
        else:
            messages.error(self.request, "There was an error in your signup. Please check your inputs.")
        return super().form_invalid(form)
    
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('staff_dashboard')
            return redirect('apply_for_passport')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# View for User Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

# View for User Dashboard (accessible only to regular users)
@login_required
def dashboard(request):
    if request.user.is_staff:
        messages.warning(request, "Staff members cannot access the regular dashboard.")
        return redirect('staff_dashboard')
    return render(request, 'dashboard.html')

# Custom decorator to check if the user is a staff member
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_active and u.is_staff, login_url=login_url)

# View for Staff Dashboard (accessible only to staff members)
@login_required
@staff_required(login_url='login')
def staff_dashboard(request):
    context = {}
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('login')
    
    # Add any additional context or data needed for the staff dashboard
    return render(request, 'registration/staff_dashboard.html', context)

from django.shortcuts import redirect
from django.contrib import messages

def staff_required(login_url=None):
    def decorator(view_func):
        @login_required(login_url=login_url)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_staff and request.user.is_active:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You must be a staff member to access this page.")
                return redirect(login_url or 'login')
        return _wrapped_view
    return decorator

def apply_for_passport(request):
    if request.method == 'POST':
        form = PassportApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print(form.errors)  # Add this to see form validation errors
    else:
        form = PassportApplicationForm()

    return render(request, 'application_form.html', {'form': form})

def success(request):
    return render(request, 'success.html')
