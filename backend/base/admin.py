from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Entrepreneur, Investor, Project, Media, Investment, Payment



@admin.register(User)
class ProjectAdmin(UserAdmin):
    list_display = ('title', 'creator', 'status', 'goal_amount', 'current_amount')
    list_filter = ('status',)
    search_fields = ('title', 'description')

# Register other models
admin.site.register(Entrepreneur)
admin.site.register(Investor)
admin.site.register(Media)
admin.site.register(Investment)
admin.site.register(Payment)