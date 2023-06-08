from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User


def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password1")
			user = authenticate(username = username, password = password)
			login(request, user)
			return redirect('home')

		else:
			return render(request, 'register.html', {'form': form})
	else:
		form = UserRegisterForm()
		return render(request, 'register.html', {'form': form})


def user_login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data = request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('home')
		else:
			form.add_error(None, 'Invalid username or password')
			return render(request, 'login.html', {'form': form})
	else:
		form = AuthenticationForm()
		return render(request, 'login.html', {'form': form})

def user_logout(request):
	logout(request)
	return redirect('home')

def staff_members(request):
	staff_profiles = UserProfile.objects.filter(user__is_staff=True)
	return render(request, 'staff.html', {'staff_profiles': staff_profiles})

def users(request):
	users = User.objects.all()
	return render(request, 'users.html', {'users': users})

def view_profile(request):
	return render(request, 'profile.html')