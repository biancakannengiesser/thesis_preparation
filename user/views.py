from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User
from courses.models import QuizCompletion
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.db import transaction, IntegrityError, DatabaseError
import logging

logger = logging.getLogger(__name__)

def register(request):
    try:
        if request.method == "POST":
            #raise ValueError("test")
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'register.html', {'form': form})
        else:
            form = UserRegisterForm()
            return render(request, 'register.html', {'form': form})
    except Exception as e:
        logger.exception('An unexpected error occurred: %s', str(e))
        return render(request, '500.html')


def user_login(request):
    try:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
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
    except Exception as e:
        logger.exception('An unexpected error occured: %s', str(e))
        return render(request, '500.html')


def user_logout(request):
	logout(request)
	return redirect('home')


def staff_members(request):
    try:
        staff_profiles = UserProfile.objects.filter(user__is_staff=True)
    except DatabaseError as e:
        logger.error('Database error occurred: %s', str(e))
        return render(request, '500.html')
    return render(request, 'staff.html', {'staff_profiles': staff_profiles})


def users(request):
	users = User.objects.all()
	return render(request, 'users.html', {'users': users})


def view_profile_as_admin(request, user_id):
	user = get_object_or_404(User, id=user_id)
	quiz_completions = QuizCompletion.objects.filter(user=request.user)
	return render(request, 'view_profile_as_admin.html', {'user':user, 'quiz_completions': quiz_completions})


@login_required
def view_profile(request):
	quiz_completions = QuizCompletion.objects.filter(user=request.user)
	return render(request, 'profile.html', {'quiz_completions': quiz_completions})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                #raise ValueError("This is a test.")
                user = request.user
                user_profile = user.userprofile

                # check if username already exists
                username = request.POST.get('username')
                if username:
                    if username != user.username:
                        if User.objects.filter(username=username).exists():
                            messages.error(request, 'Username already exists. Please enter a different one.')
                            return redirect('edit_profile')
                        else:
                            user.username = username
                    else:
                        messages.error(request, 'You have entered the same username as your current one. Please enter a different one.')
                        return redirect('edit_profile')

                # check if email already exists
                email = request.POST.get('email')
                if email:
                    if email != user.email:
                        if User.objects.filter(email=email).exists():
                            messages.error(request, 'Email already exists. Please enter a different one.')
                            return redirect('edit_profile')
                        else:
                            user.email = email
                    else:
                        messages.error(request, 'You have entered the same email as your current one. Please enter a different one.')
                        return redirect('edit_profile')

                first_name = request.POST.get('first_name')
                if first_name and first_name != user.first_name:
                    user.first_name = first_name

                last_name = request.POST.get('last_name')
                if last_name and last_name != user.last_name:
                    user.last_name = last_name

                phone = request.POST.get('phone')
                if phone and phone != user_profile.phone:
                    user_profile.phone = phone

                profile_picture = request.FILES.get('profile_picture')
                if profile_picture:
                    user_profile.image = profile_picture

                current_password = request.POST.get('current_password')
                new_password = request.POST.get('new_password')

                if current_password and new_password:
                    if user.check_password(current_password):
                        if current_password == new_password:
                            messages.error(request, 'The new password is identical to the old password. Please try again.')
                            return redirect('edit_profile')
                        else:
                            user.set_password(new_password)
                            user.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Password changed successfully')
                            return redirect('profile')
                    else:
                        messages.error(request, 'The entered current password is incorrect.')
                        return redirect('edit_profile')

                user.save()
                user_profile.save()

                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        except IntegrityError:
            logger.exception('There was an error saving your profile.')
            messages.error(request, 'There was an error saving your profile. Please try again.')
            return redirect('edit_profile')
        except Exception as e:
            logger.exception('An unexpected error occurred: %s', str(e))
            #print(str(e))
            messages.error(request, 'An unexpected error occurred. Please try again.')
            return redirect('edit_profile')

    return render(request, 'edit_profile.html')
