from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = "home"),
	path('edit_content', views.edit_content, name = "edit_content"),
	path('edit_courses', views.edit_courses, name = "edit_courses"),
	path('edit_lessons', views.edit_lessons, name = "edit_lessons"),
	path('edit_quizzes', views.edit_quizzes, name = "edit_quizzes"),
	path('add_lessons', views.add_lessons, name = "add_lessons"),
	path('add_quiz', views.add_quiz, name = "add_quiz"),
	path('add_course', views.add_course, name = "add_course"),

]