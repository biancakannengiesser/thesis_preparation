from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import TeamMemberRequest, UserProfile

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(required = True)
    image = forms.ImageField(required=False)
    subject = forms.CharField(max_length=50, required=False)
    phone = forms.CharField(max_length=10, required=True, help_text='Required. Enter a valid phone number')


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2', 'image', 'subject', 'phone']

class NewTeamMemberRequestForm(forms.ModelForm):
    class Meta:
        model = TeamMemberRequest
        verbose_name = "Team Member Request"
        verbose_name_plural = "Team Member Requests"
        fields = ['first_name', 'last_name', 'phone_number', 'email_address', 'motivation', 'resume']
    resume = forms.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'docx'], message='Only PDF or DOCX files are allowed.')
    ])