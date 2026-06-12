from django.urls import path
from . import views

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path('profile/', views.profile_view, name='profile'),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add/", views.todo_add, name="todo_add"),
    path("toggle/<int:pk>/", views.todo_toggle, name="todo_toggle"),
    path("delete/<int:pk>/", views.todo_delete, name="todo_delete"),
]
