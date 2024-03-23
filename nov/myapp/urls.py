from django.urls import path
from . import views
from .views import (delete_group, update_group, check, update_client,users_activity_view, delete_client,
                    edit_subscription, subscription_list, coach_list, add_coach,add_group,group_list,
                    add_client, add_subscription, client_list, checkcouch)

from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('student_list/', add_client, name='student_list'),
    path('students_oll/', client_list, name='client_list'),

    path('add_group/', add_group, name='add_group'),
    path('group_list/', group_list, name='group_list'),

    path('add_coach/', add_coach, name='add_coach'),
    path('coach_list/', coach_list, name='coach_list'),

    path('add_subscription/', add_subscription, name='add_subscription'),
    path('subscription_list/', subscription_list, name='subscription_list'),
    path('subscriptions/<int:subscription_id>/edit/', edit_subscription, name='edit_subscription'),

    path('client/<int:id>/update/', update_client, name='update_client'),
    path('client/<int:id>/delete/', delete_client, name='delete_client'),

    path('group/<int:id>/update/', update_group, name='update_group'),
    path('group/<int:id>/delete/', delete_group, name='delete_group'),

    path('', views.home, name='home'),


    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/get/', user_views.logout_get, name='logout'),  # Новый URL для GET запроса

    path('users-activity/', users_activity_view, name='users_activity'),

    path('update_subscription/<int:subscription_id>/<str:action>/', views.update_subscription,
         name='update_subscription'),

    path('check/', check, name='check'),

    path('checkcouch/', checkcouch, name='checkcouch'),

]