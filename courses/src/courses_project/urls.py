"""
URL configuration for courses_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from courses_app.views import CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('', RedirectView.as_view(url='/courses/', permanent=True)),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/new/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
]
