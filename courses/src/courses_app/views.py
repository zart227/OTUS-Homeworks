from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Course

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = ['name', 'description', 'instructor', 'start_date', 'end_date']

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = ['name', 'description', 'instructor', 'start_date', 'end_date']

class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('course-list')
