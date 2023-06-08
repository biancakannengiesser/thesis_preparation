from django.contrib import admin
from .models import Course, Image, Video, Lesson, Quiz, QuizOption

class QuizOptionInline(admin.TabularInline):  
    model = QuizOption
    extra = 0 

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizOptionInline]

class QuizInline(admin.TabularInline): 
    model = Quiz
    extra = 0 
    show_change_link = True

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuizInline]

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    show_change_link = True

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'description')
    inlines = [LessonInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizOption)
