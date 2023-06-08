from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Course(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True)
    description = models.TextField()
    specific_content = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.teacher is None:
            self.teacher = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True)).first()
        super().save(*args, **kwargs)

    def __str__(self):  # New method
        return self.title

class Image(models.Model):
    course = models.ForeignKey(Course, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return f"{self.course.title} Image({self.id})"


class Video(models.Model):
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    url = models.URLField()  # Use URLField to store YouTube video URLs

    def __str__(self):
        return f"{self.course.title} Video({self.id})"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    # any other lesson-specific data you have

    def __str__(self):
        return f"{self.course} - {self.title}"

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return f"{self.lesson.title} Quiz({self.id})" 

class QuizOption(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quiz.question} Option({self.id})"