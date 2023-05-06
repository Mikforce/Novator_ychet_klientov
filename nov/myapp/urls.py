from django.urls import path
from . import views
from .views import teacher_list, student_list, administrator, add_lesson

urlpatterns = [
    path('teachers/', teacher_list, name='teacher_list'),
    path('students/', student_list, name='student_list'),
    path('administrator/', administrator, name='administrator'),
    path('add-lesson/', add_lesson, name='add_lesson'),
]