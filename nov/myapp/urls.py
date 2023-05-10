from django.urls import path
from . import views
from .views import subscription_list, admin_list, coach_list, add_coach,add_group,group_list, add_client, add_admin, add_subscription, client_list

urlpatterns = [

    path('student_list/', add_client, name='student_list'),
    path('students_oll/', client_list, name='client_list'),

    path('add_group/', add_group, name='add_group'),
    path('group_list/', group_list, name='group_list'),

    path('add_coach/', add_coach, name='add_coach'),
    path('coach_list/', coach_list, name='coach_list'),

    path('admin_list/', admin_list, name='admin_list'),
    path('add_admin/', add_admin, name='add_admin'),

    path('add_subscription/', add_subscription, name='add_subscription'),
    path('subscription_list/', subscription_list, name='subscription_list'),

]