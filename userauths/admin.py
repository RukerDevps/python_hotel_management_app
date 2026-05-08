from django.contrib import admin
from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'username']  # Assuming 'full_name' and 'username' are fields in the User model
    list_display = ['username', 'full_name', 'email', 'phone', 'gender']

admin.site.register(User, UserAdmin)  # Register User model with UserAdmin

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'user__username']  # Assuming 'full_name' is a field in the Profile model and 'user__username' is a field related to the User model
    list_display = ['full_name', 'user', 'verified']

admin.site.register(Profile, ProfileAdmin)  # Register Profile model with ProfileAdmin
