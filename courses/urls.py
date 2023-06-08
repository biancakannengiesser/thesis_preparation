from django.urls import path
from . import views

urlpatterns = [
	path('courses', views.courses, name = "courses"),
	path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
]