from django import forms
from courses.models import Course, Lesson, Quiz, QuizOption, Image
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import ProblemReport, Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['username', 'testimonial']

class ReportProblemForm(forms.ModelForm):
    class Meta:
        model = ProblemReport
        fields = ['name', 'email', 'message']


class LessonForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'audio_file']
        widgets = {
            'title': forms.Textarea(attrs={'rows': 1, 'cols': 90}),
            'content' : forms.Textarea(attrs={'rows': 8, 'cols': 90})
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['lesson', 'question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 70}),
        }
class QuizOptionForm(forms.ModelForm):
    id = forms.ModelChoiceField(queryset=QuizOption.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = QuizOption
        fields = ['id', 'answer', 'is_correct']
        labels = {
            'answer' : "Answer Option",
        }

class CourseForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))
    class Meta:
        model = Course
        fields = ['title', 'image', 'gif', 'description', 'specific_content', 'teacher']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 70}),
            'specific_content': forms.Textarea(attrs={'rows': 3, 'cols': 70}),
        }
        labels = {
            'image': 'Course Image',
            'gif': 'Background Image Quiz',
            'description': 'Course Description',
            'specific_content' : 'Course Content'
        }

QuizOptionFormset = inlineformset_factory(Quiz, QuizOption, fields=('answer', 'is_correct'), extra=4, max_num=4)
ImageFormSet = inlineformset_factory(Course, Image, fields=('image',), extra=7, max_num=7)