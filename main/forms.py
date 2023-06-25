from django import forms
from courses.models import Course, Lesson, Quiz, QuizOption, Image
from django.forms import inlineformset_factory

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['lesson', 'question']

class QuizOptionForm(forms.ModelForm):
    class Meta:
        model = QuizOption
        fields = ['answer', 'is_correct']
        labels = {
            'answer' : "Answer Option",
        }

class CourseForm(forms.ModelForm):
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
ImageFormSet = inlineformset_factory(Course, Image, fields=('image',), extra=3, max_num=7)