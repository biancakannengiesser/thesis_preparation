from django.db import models

# Create your models here.
class ProblemReport(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

class Testimonial(models.Model):
    username = models.CharField(max_length=100)
    testimonial = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username