from django.shortcuts import render, redirect, get_object_or_404
from user.forms import NewTeamMemberRequestForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages 
from courses.models import Course, Image, Video, Lesson, Quiz, QuizOption
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .forms import LessonForm, QuizForm, QuizOptionForm, CourseForm, ImageFormSet, QuizOptionFormset, ReportProblemForm, TestimonialForm
from django.http import HttpResponse
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from .models import ProblemReport, Testimonial


def report_problem(request):
    if request.method == "POST":
        form = ReportProblemForm(request.POST)
        if form.is_valid():
            report = form.save()
            subject = "Website Problem Reported"
            message = form.cleaned_data.get('message')
            sender = form.cleaned_data.get('email')
            recipients = [settings.EMAIL_HOST_USER]
            #send mail
            email = EmailMessage(subject, message, sender, recipients)
            num_sent = email.send()

            #print(f"nr of emails sent: {num_sent}")
            messages.success(request, "Your problem report has been sent!")
            return redirect('home')
    else:
        form = ReportProblemForm()
    return render(request, 'home.html', {'report_problem_form': form})

@login_required
def reported_problems(request):
    all_reports = ProblemReport.objects.all()
    return render(request, 'reported_problems.html', {'all_reports': all_reports})


def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = TestimonialForm(request.POST)
            if form.is_valid():
                entered_username = form.cleaned_data.get('username')
                if entered_username != request.user.username:
                    messages.error(request, "The entered username does not match the logged-in user. Please try again.")
                    return redirect('home')
                else:
                    form.save()
                    messages.success(request, 'Thank you for your testimonial!')
                    return redirect('home')
        else:
            form = TestimonialForm()
        name = request.user.first_name
        testimonials = Testimonial.objects.order_by('-date_posted')
        testimonials_count = testimonials.count()
        return render(request, 'home.html', {'form': form, 'testimonials': testimonials, 'name': name, 'testimonials_count': testimonials_count})
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
        course = None 
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
            if key.startswith('new_image_'):
                # This is a new image, create a new Image instance
                image_file = request.FILES.get(key)
                if course is not None:
                    Image.objects.create(course=course, image=image_file)
                else:
                    messages.error(request, 'Could not create new image - no associated course.')
                    return redirect('edit_courses')
            elif key.startswith('image_'):
                # update existing image
                image_id = "_".join(key.split('_')[1:])
                image_file = request.FILES.get(key)
                try:
                    image = Image.objects.get(id=image_id)
                    image.image = image_file
                    image.save()
                except Image.DoesNotExist:
                    messages.error(request, 'Could not update image - image not found.')
                    return redirect('edit_courses')

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
        for key, value in request.POST.items():
            #print(key, value)
            if key.startswith('lesson-'):
                _, lesson_id, field = key.split('-')

                if field == 'delete' and value == 'on':
                    lesson = Lesson.objects.get(pk=lesson_id)
                    lesson.delete()
                else:
                    lesson = Lesson.objects.get(pk=lesson_id)

                    form_data = {
                        'title': request.POST.get(f"lesson-{lesson_id}-title"),
                        'content': request.POST.get(f"lesson-{lesson_id}-content"),
                        'course': request.POST.get(f"lesson-{lesson_id}-course"),
                    }

                    form = LessonForm(form_data, instance=lesson)

                    if not form.is_valid():
                        print(form.errors)
                        return HttpResponse('Form is invalid', status=400)

                    # check delete box
                    if request.POST.get(f"lesson-{lesson_id}-delete_audio") == 'on':
                        lesson.audio_file.delete()  # delete the audio file

                    # check for audio
                    audio_file = request.FILES.get(f"lesson-{lesson_id}-audio_file")
                    if audio_file is not None:
                        lesson.audio_file = audio_file
                        lesson.save()

                    else:
                        #print("nu")
                        pass

                    form.save()

        messages.success(request, 'Lessons updated successfully!')
        return redirect('edit_lessons')

    else:
        courses = Course.objects.all()
        lesson_forms = [(course, [LessonForm(instance=lesson) for lesson in course.lesson_set.all()]) for course in courses]
        return render(request, 'edit_lessons.html', {'lesson_forms': lesson_forms})




def edit_quizzes(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            print(key)
            if key.startswith('quiz-'):
                _, quiz_id, field = key.split('-')
                
                if field == 'delete' and value == 'on':
                    quiz = Quiz.objects.get(pk=quiz_id)
                    quiz.delete()
                else:
                    quiz = Quiz.objects.get(pk=quiz_id)
                    form_data = {
                        'question': request.POST.get(f"quiz-{quiz_id}-question"),
                        'lesson': quiz.lesson_id,
                    }

                    form = QuizForm(form_data, instance=quiz)
                    if form.is_valid():
                        form.save()
                    else:
                        print(form.errors)
                        return HttpResponse('Form is invalid', status=400)

            elif key.startswith('option-'):
                _, option_id, field = key.split('-')
                print(option_id)
                option = QuizOption.objects.get(pk=option_id)

                if field == 'delete':
                    if value == 'on':
                        option.delete()
                        continue

                form_data = {
                    'id': option_id,
                    'answer': request.POST.get(f"option-{option_id}-answer"),
                    'is_correct': request.POST.get(f"option-{option_id}-is_correct"),
                }

                form = QuizOptionForm(form_data, instance=option)
                print("option:", option)
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)
                    return HttpResponse('Form is invalid', status=400)

        messages.success(request, 'Quizzes updated successfully!')
        return redirect('edit_quizzes')

    else:
        courses = Course.objects.all()
        quiz_forms = []
        for course in courses:
            course_forms = []
            for quiz in course.quiz_set.all():
                quiz_form = QuizForm(instance=quiz)
                quiz_option_formset = QuizOptionFormset(instance=quiz)
                course_forms.append((quiz_form, quiz_option_formset))
            quiz_forms.append((course, course_forms))

        return render(request, 'edit_quizzes.html', {'quiz_forms': quiz_forms})



def add_lessons(request):
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
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
            messages.success(request, "Course added successfully!")
            return redirect('add_course')
    else:
        form = CourseForm()
        formset = ImageFormSet(prefix='images')


    courses = Course.objects.all()
    return render(request, 'add_course.html', {'form': form, 'formset': formset, 'courses':courses})