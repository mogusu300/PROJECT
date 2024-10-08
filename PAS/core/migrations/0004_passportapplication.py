# Generated by Django 5.1 on 2024-09-05 11:52

import django_countries.fields
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_customuser_email_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassportApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=100)),
                ('other_names', models.CharField(max_length=200)),
                ('age_at_last_birthday', models.IntegerField()),
                ('date_of_birth', models.DateField()),
                ('place_of_birth', models.CharField(max_length=100)),
                ('country_of_birth', django_countries.fields.CountryField(max_length=2)),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')], max_length=50)),
                ('maiden_surname', models.CharField(blank=True, max_length=100, null=True)),
                ('name_changed', models.BooleanField(default=False)),
                ('original_name', models.CharField(blank=True, max_length=100, null=True)),
                ('personal_address', models.CharField(max_length=255)),
                ('usual_place_of_residence', models.CharField(max_length=255)),
                ('place_of_birth_parent', models.CharField(max_length=100)),
                ('country_of_birth_parent', django_countries.fields.CountryField(max_length=2)),
                ('national_status_of_parent', django_countries.fields.CountryField(max_length=2)),
                ('profession_or_occupation', models.CharField(max_length=100)),
                ('residence_country', django_countries.fields.CountryField(max_length=2)),
                ('height', models.DecimalField(decimal_places=2, max_digits=4)),
                ('color_of_eyes', models.CharField(max_length=50)),
                ('color_of_hair', models.CharField(max_length=50)),
                ('special_peculiarities', models.TextField(blank=True, null=True)),
                ('residential_address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('national_id_number', models.CharField(blank=True, max_length=20, null=True)),
                ('drivers_license_number', models.CharField(blank=True, max_length=20, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=20, null=True)),
                ('parent_guardian_name', models.CharField(max_length=255)),
                ('parent_guardian_nationality', django_countries.fields.CountryField(max_length=2)),
                ('parent_guardian_birthplace', models.CharField(max_length=255)),
                ('parent_guardian_contact_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('parent_guardian_residential_address', models.TextField(blank=True, null=True)),
                ('parent_guardian_relationship', models.CharField(blank=True, max_length=100, null=True)),
                ('passport_type', models.CharField(choices=[('ordinary_32', 'Ordinary 32 pages'), ('ordinary_48', 'Ordinary 48 pages'), ('diplomatic', 'Diplomatic')], max_length=20)),
                ('reason_for_passport', models.CharField(choices=[('new', 'New Passport'), ('renewal', 'Renewal'), ('lost', 'Lost Passport')], max_length=20)),
                ('service_type', models.CharField(choices=[('express', 'Express'), ('live_photo', 'Live Photograph')], max_length=20)),
                ('citizenship_proof_type', models.CharField(max_length=100)),
                ('citizenship_proof', models.FileField(blank=True, null=True, upload_to='citizenship_proofs/')),
                ('photograph', models.ImageField(upload_to='passport_photos/')),
            ],
        ),
    ]
