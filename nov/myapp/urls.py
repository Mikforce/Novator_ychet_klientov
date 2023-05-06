from django.urls import path
from . import views

app_name = 'my_app'

urlpatterns = [

    path('teachers/', views.teacher_list, name='add_teacher'),

    path('students/', views.student_list, name='student_list'),
    path('administrators/', views.administrator, name='administrator_list'),
]
