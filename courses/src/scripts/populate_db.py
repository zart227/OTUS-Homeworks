import os
import sys
import django

# Добавляем путь к папке src в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Устанавливаем переменные окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courses_project.settings')
django.setup()

from courses_app.models import Instructor, Student, Course, Schedule

def populate():
    # Очистите текущие данные (опционально)
    Instructor.objects.all().delete()
    Student.objects.all().delete()
    Course.objects.all().delete()
    Schedule.objects.all().delete()
    
    # Создание преподавателей
    instructor1 = Instructor(name='John Doe', email='john.doe@example.com')
    instructor2 = Instructor(name='Jane Smith', email='jane.smith@example.com')
    instructor1.save()
    instructor2.save()

    # Создание студентов
    student1 = Student(name='Alice Johnson', email='alice.johnson@example.com')
    student2 = Student(name='Bob Brown', email='bob.brown@example.com')
    student1.save()
    student2.save()

    # Создание курсов
    course1 = Course(name='Python Basics', description='Introduction to Python programming.', instructor=instructor1, start_date='2024-01-01', end_date='2024-03-01')
    course2 = Course(name='Django for Beginners', description='Learn how to build web applications with Django.', instructor=instructor2, start_date='2024-02-01', end_date='2024-04-01')
    course1.save()
    course2.save()

    # Создание расписаний
    schedule1 = Schedule(course=course1, student=student1, date='2024-01-15')
    schedule2 = Schedule(course=course2, student=student2, date='2024-02-15')
    schedule1.save()
    schedule2.save()

    print("Database has been populated with initial data.")

if __name__ == '__main__':
    populate()
