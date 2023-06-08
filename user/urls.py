from django.urls import path
from . import views

urlpatterns = [
	path('register', views.register, name = "register"),
	path('login', views.user_login, name = "login"),
	path('logout', views.user_logout, name = "logout"),
	path('staff', views.staff_members, name = "staff"),
	path('users', views.users, name = "users"),
	path('profile', views.view_profile, name = "profile"),


]

