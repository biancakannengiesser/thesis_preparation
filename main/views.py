from django.shortcuts import render, redirect
from user.forms import NewTeamMemberRequestForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages 
from courses.models import Course, Image, Video, Lesson, Quiz, QuizOption
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .forms import LessonForm, QuizForm, QuizOptionForm, CourseForm, ImageFormSet, QuizOptionFormset




# Create your views here.

def index(request):
    if request.user.is_authenticated:
        name = request.user.first_name
        return render(request, 'home.html', {'name': name})
    else:
        if request.method == "POST":
            form = NewTeamMemberRequestForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                except Exception as e:
                    logger.exception('An unexpected error occurred while saving the form: %s', str(e))
                    messages.error(request, "There was a problem saving your form. Please try again.")
                    return render(request, 'home.html', {'form': form})

                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                email = form.cleaned_data.get("email_address")
                phone_number = form.cleaned_data.get("phone_number")
                motivation = form.cleaned_data.get("motivation")
                resume = request.FILES['resume']

                msg = f'New request from:\n\n Name: {last_name} {first_name}\nPhone Number: {phone_number}\n Motivation message: {motivation}\n'

                email = EmailMessage(
                    "New Team Member Request",  #subject
                    msg,                        #message
                    email,                      #sender
                    [settings.EMAIL_HOST_USER]  #receiver
                    )

                email.attach(resume.name, resume.read(), resume.content_type)

                try:  
                    email.send()
                except Exception as e:
                    logger.exception('An unexpected error occurred while sending the email: %s', str(e))
                    messages.error(request, "There was a problem sending your email. Please try again.")
                    return render(request, 'home.html', {'form': form})

                messages.success(request, "Thank you for submitting your application! We received your request and will respond shortly.")

                return redirect('home')
            else: 
                form.add_error(None, 'Invalid username or password')
                has_errors = True
                return render(request, 'home.html', {'form': form, 'has_errors': has_errors})
        else:
            form = NewTeamMemberRequestForm()
        return render(request, 'home.html', {'form': form})


def edit_content(request):
    return render(request, 'edit_content.html')


def edit_courses(request):
    if request.method == "POST":
        for key in request.POST:
            if key.startswith('course-'):
                _, course_id, field = key.split('-')
                course = Course.objects.get(pk=course_id)
                if field == 'title':
                    course.title = request.POST.get(key)
                elif field == 'description':
                    course.description = request.POST.get(key)
                elif field == 'specific_content':
                    course.specific_content = request.POST.get(key)
                elif field == 'teacher':
                    teacher_id = request.POST.get(key)
                    teacher = User.objects.get(pk=teacher_id)
                    course.teacher = teacher
                elif field == 'video_url':
                    video_url = request.POST.get(key)
                    validate = URLValidator()
                    try:
                        validate(video_url)  # check if url is valid
                        video = course.videos.first()
                        if video:
                            video.url = video_url
                            video.save()
                        else:
                            # create a new video if no video exists
                            Video.objects.create(course=course, url=video_url)
                    except ValidationError:
                        messages.error(request, 'Invalid URL for Video!')
                        return redirect('edit_courses')
                if 'image' in request.FILES:
                    course.image = request.FILES['image']
                if 'delete_image' in request.POST:
                    course.image.delete()
                if 'gif' in request.FILES:
                    course.gif = request.FILES['gif']
                if 'delete_gif' in request.POST:
                    course.gif.delete()

                course.save()

        for key in request.FILES:
            if key.startswith('image_'):
                image_id = "_".join(key.split('_')[1:])
                image_file = request.FILES.get(key)
                # find img by id
                try:
                    image = Image.objects.get(id=image_id)
                    #if found, update it
                    image.image = image_file
                    image.save()
                except Image.DoesNotExist:
                    # if not found, create a new one
                    Image.objects.create(course=course, image=image_file)

        for key in request.POST:
            if key.startswith('delete_image_'):
                _, _, image_id = key.split('_')
                if request.POST.get(key) == 'on':
                    try:
                        image = Image.objects.get(id=image_id)
                        image.delete()
                    except Image.DoesNotExist:
                        pass

        messages.success(request, 'Courses updated successfully!')
        return redirect('edit_courses')

    else:
        courses = Course.objects.all()
        staff_users = User.objects.filter(is_staff=True)
        return render(request, 'edit_courses.html', {'courses': courses, 'staff_users': staff_users})


def edit_lessons(request):
    if request.method == "POST":
        for key in request.POST:
            if key.startswith('lesson-'):
                _, lesson_id, field = key.split('-')
                lesson = Lesson.objects.get(pk=lesson_id)

                if field == 'title':
                    lesson.title = request.POST.get(key)
                elif field == 'content':
                    lesson.content = request.POST.get(key)
                elif field == 'delete':
                    if request.POST.get(key) == 'on':
                        lesson.delete()
                        continue  # Skip saving, since we just deleted the lesson
                
                lesson.save()

        messages.success(request, 'Lessons updated successfully!')
        return redirect('edit_lessons')

    else:
        courses = Course.objects.all()
        return render(request, 'edit_lessons.html', {'courses': courses})


def edit_quizzes(request):
    courses = Course.objects.all()
    if request.method == "POST":
        # Loop through quizzes in the post data
        for key, value in request.POST.items():
            if key.startswith("quiz"):
                # Extract the quiz id
                quiz_id = int(key.split('-')[1])
                quiz = Quiz.objects.get(id=quiz_id)

                # Update quiz question
                if key.endswith("question"):
                    quiz.question = value

                # Check if the quiz should be deleted
                elif key.endswith("delete"):
                    if value.lower() == "on":
                        quiz.delete()
                        continue

                quiz.save()

            elif key.startswith("option"):
                # Extract the option id
                option_id = int(key.split('-')[1])
                option = QuizOption.objects.get(id=option_id)

                # Update option answer
                if key.endswith("answer"):
                    option.answer = value

                # Check if the option should be deleted
                elif key.endswith("delete"):
                    if value.lower() == "on":
                        option.delete()
                        continue

                # Check if the option is the correct answer
                elif key.endswith("is-correct"):
                    if value.lower() == "on":
                        option.is_correct = True
                    else:
                        option.is_correct = False

                option.save()

            elif key.startswith("new-option"):
                # Extract the option number
                option_number = int(key.split('-')[2])

                # Initialize is_correct to False
                is_correct = False

                # Update option answer
                if key.endswith("answer"):
                    answer = value

                # Check if the option is the correct answer
                elif key.endswith("is-correct"):
                    if value.lower() == "on":
                        is_correct = True

                # Create new QuizOption
                new_option = QuizOption(answer=answer, quiz=quiz, is_correct=is_correct)
                new_option.save()

        messages.success(request, "Changes saved successfully")
        return redirect('edit_quizzes')

    return render(request, 'edit_quizzes.html', {'courses': courses})


def add_lessons(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lesson added successfully!")
            return redirect('add_lessons')
    else:
        form = LessonForm()
    lessons = Lesson.objects.all()  # Fetch all lessons from the database
    return render(request, 'add_lessons.html', {'form': form, 'lessons': lessons})

def add_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save()
            formset = QuizOptionFormset(request.POST, instance=quiz)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Quiz added successfully!")
                return redirect('add_quiz')
    else:
        quiz_form = QuizForm()
        formset = QuizOptionFormset()

    quizzes = Quiz.objects.prefetch_related('quizoption_set').all()  # Fetch all quizzes and their options
    return render(request, 'add_quiz.html', {'quiz_form': quiz_form, 'formset': formset, 'quizzes': quizzes})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, prefix='images')
        if form.is_valid() and formset.is_valid():
            course = form.save()
            formset.instance = course
            formset.save()
            return redirect('add_course')
    else:
        form = CourseForm()
        formset = ImageFormSet(prefix='images')


    courses = Course.objects.all()
    return render(request, 'add_course.html', {'form': form, 'formset': formset, 'courses':courses})