# Generated by Django 5.1 on 2024-09-05 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_passportapplication_citizenship_proof_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passportapplication',
            name='place_of_birth',
        ),
    ]
