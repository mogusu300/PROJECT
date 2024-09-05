# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,PassportApplication
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(max_length=255, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(max_length=255, required=True, help_text='Required. Enter your email address.')

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

from django import forms
from .models import PassportApplication
from phonenumber_field.formfields import PhoneNumberField

class PassportApplicationForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=True)
    parent_guardian_contact_number = PhoneNumberField(required=True)

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'})
    )

    class Meta:
        model = PassportApplication
        fields = '__all__'
        labels = {
            'name_changed': 'Has your name been changed? (Otherwise than by marriage)',
            'original_name': 'If so, state original name',
            'height': 'Height',
        }
        widgets = {
            'passport_type': forms.Select(),
            'reason_for_passport': forms.Select(),
            'service_type': forms.Select(),
            'height': forms.NumberInput(attrs={'placeholder': 'Enter height in meters (e.g., 1.75)'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'citizenship_proof': forms.ClearableFileInput(attrs={'accept': 'image/*,.pdf,.doc,.docx'})
        }

    def clean(self):
        cleaned_data = super().clean()
        national_id_number = cleaned_data.get("national_id_number")
        drivers_license_number = cleaned_data.get("drivers_license_number")

        # Ensure one and only one of the fields is provided
        if not national_id_number and not drivers_license_number:
            raise forms.ValidationError("Please provide either a National ID number or a Driver's License number.")
        if national_id_number and drivers_license_number:
            raise forms.ValidationError("You cannot provide both a National ID number and a Driver's License number.")