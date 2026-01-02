from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone', 'email_verified', 'phone_verified', 'is_staff']
    list_filter = ['email_verified', 'phone_verified', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    inlines = [UserProfileInline]
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'date_of_birth', 'profile_image', 'email_verified', 'phone_verified')}),
    )
