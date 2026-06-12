from django.contrib import admin
from .models import Todo, Profile

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["title", "completed", "user", "created_at"]
    list_filter = ["completed", "created_at"]
    search_fields = ["title"]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']
