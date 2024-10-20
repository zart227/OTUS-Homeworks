from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django_rq import get_queue
from .forms import ContactForm
from rq import Queue
from .tasks import send_contact_email
from .models import Course, Instructor

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        return Course.objects.select_related('instructor') 
    
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
     
    def get_queryset(self):
        return Course.objects.select_related('instructor') 
 
class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = ['name', 'description', 'instructor', 'start_date', 'end_date']
    success_url = reverse_lazy('course-list') 

class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/course_form.html'
    fields = ['name', 'description', 'instructor', 'start_date', 'end_date']
     
    def get_queryset(self):
        return Course.objects.select_related('instructor') 
    
    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={'pk': self.object.pk})
    
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('course-list')

class InstructorDetailView(DetailView):
    model = Instructor
    template_name = 'courses/instructor_detail.html'
    context_object_name = 'instructor'

    def get_queryset(self):
        return Instructor.objects.prefetch_related('course_set')
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.object.course_set.all()
        return context


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Отправляем сообщения в очередь
            queue = get_queue('default')
            queue.enqueue(send_contact_email, email, name, message)
            
            return redirect('contact-success')
    else:
        form = ContactForm()
    
    return render(request, 'courses/contact.html', {'form': form})


def contact_success_view(request):
    return render(request, 'courses/contact_success.html')
