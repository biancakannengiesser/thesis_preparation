from django.urls import path
from . import views

urlpatterns = [
	path('register', views.register, name = "register"),
	path('login', views.user_login, name = "login"),
	path('logout', views.user_logout, name = "logout"),
	path('staff', views.staff_members, name = "staff"),
	path('users', views.users, name = "users"),
	path('profile/<int:user_id>/', views.view_profile_as_admin, name='view_profile_as_admin'),
	path('profile', views.view_profile, name = "profile"),
	path('edit_profile', views.edit_profile, name = "edit_profile"),



]

