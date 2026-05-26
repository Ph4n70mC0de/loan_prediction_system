from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'role', 'status', 'is_staff', 'created_at']
    list_filter = ['role', 'status', 'is_staff', 'is_superuser']
    search_fields = ['email', 'username', 'phone_number']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('role', 'status', 'phone_number', 'date_of_birth', 'mfa_enabled', 'mfa_secret')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile', {'fields': ('email', 'role', 'phone_number', 'date_of_birth')}),
    )