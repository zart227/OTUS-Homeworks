from django.contrib import admin
from .models import Instructor, Student, Course, Schedule

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
 
    def courses(self, obj):
        return ", ".join([course.name for course in obj.course_set.all()])

    courses.short_description = 'Courses'

    list_display = ('name', 'email', 'courses')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'start_date', 'end_date')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('instructor')    

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'date')
