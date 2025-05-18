from django.contrib import admin  # This import was missing
from django.contrib.auth.admin import UserAdmin
from .models import User, Entrepreneur, Investor, Project, Media, Investment, Payment

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login',)}),  # Removed date_joined
        ('BIDAYA Specific', {'fields': ('user_type',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phone', 'user_type'),
        }),
    )

# Proper registration using admin.site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Entrepreneur)
admin.site.register(Investor)
admin.site.register(Project)
admin.site.register(Media)
admin.site.register(Investment)
admin.site.register(Payment)