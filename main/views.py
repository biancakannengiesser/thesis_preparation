from django.shortcuts import render, redirect
from user.forms import NewTeamMemberRequestForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages 

# Create your views here.

def index(request):
	if request.user.is_authenticated:
		name = request.user.first_name
		return render(request, 'home.html', {'name': name})
	else:
		if request.method == "POST":
			form = NewTeamMemberRequestForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()

				#now send the email
				first_name = form.cleaned_data.get("first_name")
				last_name = form.cleaned_data.get("last_name")
				email = form.cleaned_data.get("email_address")
				phone_number = form.cleaned_data.get("phone_number")
				motivation = form.cleaned_data.get("motivation")
				resume = request.FILES['resume']

				msg = f'New request from:\n\n Name: {last_name} {first_name}\nPhone Number: {phone_number}\n Motivation message: {motivation}\n'

				email = EmailMessage(
					"New Team Member Request",	#subject
					msg, 						#message
					email,						#sender
					[settings.EMAIL_HOST_USER]	#receiver
					)

				email.attach(resume.name, resume.read(), resume.content_type)	

				email.send()

				messages.success(request, "Thank you for submitting your application! We received your request and will respond shortly.")

				return redirect('home')
			else: 
				form.add_error(None, 'Invalid username or password')
				has_errors = True
				return render(request, 'home.html', {'form': form, 'has_errors': has_errors})
		else:
			form = NewTeamMemberRequestForm()
		return render(request, 'home.html', {'form': form})