from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the primary identifier.
    """
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)  # For admin site access
    is_active = models.BooleanField(default=True)
    is_officer = models.BooleanField(default=False)  # Custom field for passport officers
    date_joined = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

class PassportApplication(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    PASSPORT_TYPES = [
        ('ordinary_32', 'Ordinary 32 pages'),
        ('ordinary_48', 'Ordinary 48 pages'),
        ('diplomatic', 'Diplomatic'),
    ]
    
    REASONS_FOR_PASSPORT = [
        ('new', 'New Passport'),
        ('renewal', 'Renewal'),
        ('lost', 'Lost Passport'),
    ]
    
    SERVICES = [
        ('express', 'Express'),
        ('live_photo', 'Live Photograph'),
    ]
    
    # Personal Details Section
    surname = models.CharField(max_length=100, default="unknown")
    other_names = models.CharField(max_length=200, default="hey")
    age_at_last_birthday = models.IntegerField(default=16)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    country_of_birth = CountryField(default="Zambia")
    marital_status = models.CharField(max_length=50, choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')])
    maiden_surname = models.CharField(max_length=100, blank=True, null=True)
    name_changed = models.BooleanField(default=False)
    original_name = models.CharField(max_length=100, blank=True, null=True)
    personal_address = models.CharField(max_length=255, default="unknown")
    usual_place_of_residence = models.CharField(max_length=255, default="lusaka")
    place_of_birth_parent = models.CharField(max_length=100, default="unknown")
    country_of_birth_parent = CountryField(default="Zambia")
    national_status_of_parent = CountryField(default="Zambia")

    # Personal Description Section
    profession_or_occupation = models.CharField(max_length=100, default="unknown")
    residence_country = CountryField(default="Zambia")
    height = models.Decimaheight = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Store height in meters 
    color_of_eyes = models.CharField(max_length=50, default="Black")
    color_of_hair = models.CharField(max_length=50, default="Black")
    special_peculiarities = models.TextField(blank=True, null=True)
    
    # Contact Information
    residential_address = models.TextField()
    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True, null=True)
    
    # Identification Details
    national_id_number = models.CharField(max_length=20, blank=True, null=True)
    drivers_license_number = models.CharField(max_length=20, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)

    # Parent/Guardian Information
    parent_guardian_name = models.CharField(max_length=255)
    parent_guardian_nationality = CountryField()
    parent_guardian_birthplace = models.CharField(max_length=255)
    parent_guardian_contact_number = PhoneNumberField(blank=True, null=True)
    parent_guardian_residential_address = models.TextField(blank=True, null=True)
    parent_guardian_relationship = models.CharField(max_length=100, blank=True, null=True)

    # Passport Information
    passport_type = models.CharField(max_length=20, choices=PASSPORT_TYPES, default="Ordinary 32 pages")
    reason_for_passport = models.CharField(max_length=20, choices=REASONS_FOR_PASSPORT, default="New Passport")
    service_type = models.CharField(max_length=20, choices=SERVICES, default="Express")

    # Proof of Citizenship
    citizenship_proof = models.FileField(upload_to='citizenship_proofs/', blank=True, null=True)

    # Photographs
    photograph = models.ImageField(upload_to='passport_photos/')

    def __str__(self):
        return self.surname

    def clean(self):
        super().clean()
        # Ensure that either National ID or Driver's License is provided, but not both
        if not self.national_id_number and not self.drivers_license_number:
            raise ValidationError('Please provide either a National ID number or a Driver\'s License number.')
        if self.national_id_number and self.drivers_license_number:
            raise ValidationError('You cannot provide both a National ID number and a Driver\'s License number.')
