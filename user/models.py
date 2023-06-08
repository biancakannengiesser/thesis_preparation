from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    subject = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    cv = models.FileField(blank = True)


class TeamMemberRequest(models.Model):
	first_name = models.CharField('First Name', max_length = 30)
	last_name = models.CharField('Last Name', max_length = 30)
	phone_number = models.CharField('Contact Phone', max_length = 10)
	email_address = models.EmailField()
	motivation = models.TextField('Motivation', max_length = 250)
	resume = models.FileField()