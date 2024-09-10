# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_officer')
    list_filter = ('is_staff', 'is_active', 'is_officer')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_officer')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_officer'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import PassportApplication

class PassportApplicationAdmin(admin.ModelAdmin):
    list_display = ('surname', 'other_names', 'date_of_birth', 'passport_type', 'service_type', 'display_photo')
    list_filter = ('passport_type', 'service_type', 'date_of_birth')
    search_fields = ('surname', 'other_names', 'passport_number')

    def display_photo(self, obj):
        if obj.photograph:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />'.format(obj.photograph.url))
        return "No Photo"

    display_photo.short_description = 'Photograph'

    # Explicitly allow deletion in admin
    def has_delete_permission(self, request, obj=None):
        return True  # Allow deletion

admin.site.register(PassportApplication, PassportApplicationAdmin)
