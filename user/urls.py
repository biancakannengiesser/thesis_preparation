from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('register', views.register, name = "register"),
	path('login', views.user_login, name = "login"),
	path('logout', views.user_logout, name = "logout"),
	path('staff', views.staff_members, name = "staff"),
	path('users', views.users, name = "users"),
	path('profile/<int:user_id>/', views.view_profile_as_admin, name='view_profile_as_admin'),
	path('profile', views.view_profile, name = "profile"),
	path('edit_profile', views.edit_profile, name = "edit_profile"),
	path('new_member_requests', views.new_member_requests, name = "new_member_requests"),
	path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

]
