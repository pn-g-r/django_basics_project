from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Todo, Profile

# Unregister the provided User admin
admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["title", "completed", "user", "created_at"]
    list_filter = ["completed", "created_at"]
    search_fields = ["title"]
