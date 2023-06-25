from django.shortcuts import render, get_object_or_404
from .models import Course, Quiz, QuizOption, QuizCompletion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import UserProfile
import json


# Create your views here.

def courses(request):
	courses = Course.objects.all()
	return render(request, 'courses.html', {'courses':courses})



@csrf_exempt
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST' and request.content_type == 'application/json':
        user_answers = json.loads(request.body)

        score = 0
        for question_id, answer_id in user_answers.items():
            correct_option = QuizOption.objects.filter(quiz__id=question_id, is_correct=True).first()
            if str(correct_option.id) == answer_id:
                score += 2

        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.total_score += score
        user_profile.save()

        # Save the course completion
        course_completion = QuizCompletion(
            user=request.user,
            course=course,  
            score=score,
        )
        course_completion.save()

        return JsonResponse({
            'message': 'Quiz submitted successfully.',
            'score': score,
        })

    return render(request, 'course_detail.html', {'course': course})