from django.shortcuts import get_object_or_404
from .models import (Group, Coach, Subscription, Client, Profile, MarkedAttendance, UserActivityLog, TrainingRoom,
                     LessonSchedule)
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import UserRegisterForm, LessonScheduleForm, TrainingRoomForm
import os
import time
from datetime import date
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db.models import Sum
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from docxtpl import DocxTemplate
from django.db import transaction
from docxtpl import DocxTemplate
from django.conf import settings
import subprocess
from django.views.generic import ListView, DetailView
from django.http import FileResponse
from django.http import HttpResponse
import io
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            login(request, user)  # Автоматический вход пользователя после регистрации
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def logout_get(request):
    if request.user.is_authenticated:
        # Сохранение даты и времени выхода пользователя
        UserActivityLog.objects.create(user=request.user, activity_type='Logged out', timestamp=timezone.now())

        logout(request)
    return redirect('home')


def get_client_by_card_number(card_number):
    try:
        client = Client.objects.get(card_number=card_number)
        return client
    except Client.DoesNotExist:
        return None


@login_required
def home(request):
    groups = Group.objects.all()
    subscriptions = Subscription.objects.all()
    markedAttendance = MarkedAttendance.objects.filter(timestamp__date=date.today())

    if 'card_number' in request.GET:
        card_number = request.GET.get('card_number')
        client = get_client_by_card_number(card_number)

        if client:
            # Redirect to the client's profile page
            return redirect('view_client_profile', id=client.id)

    return render(request, 'index.html',
                  {'groups': groups, 'subscriptions': subscriptions, 'markedAttendance': markedAttendance})




@login_required
def users_activity_view(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    users = User.objects.all()
    users_data = []

    for user in users:
        start_of_month = datetime(current_year, current_month, 1)
        end_of_month = datetime(current_year, current_month, 1) + timedelta(days=31)
        user_activity_logs = UserActivityLog.objects.filter(user=user, timestamp__range=(start_of_month, end_of_month))
        user_activity_hours = sum([(log.timestamp.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1) - log.timestamp).total_seconds() / 3600 for log in user_activity_logs])
        users_data.append({
            'user': user,
            'total_hours': round(user_activity_hours, 2)
        })

    return render(request, 'users_activity.html', {'users_data': users_data})



@login_required
def client_list(request):
    query = request.GET.get('q')

    if query:
        clients = Client.objects.filter(full_name__icontains=query)
    else:
        clients = Client.objects.all()

    return render(request, 'client_list.html', {'clients': clients})


@login_required
def add_client(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        birth_date = request.POST['birth_date']
        phone_number = request.POST['phone_number']
        parent_name = request.POST['parent_name']
        address = request.POST['address']
        card_number = request.POST['card_number']
        group_id = request.POST.get('group')
        date_joined = request.POST['date_joined']

        group_obj = Group.objects.get(id=group_id)
        client = Client(full_name=full_name, birth_date=birth_date, phone_number=phone_number, parent_name=parent_name,
                        address=address, card_number=card_number,
                        group_obj=group_obj, date_joined=date_joined)
        client.save()

        # Render client details using the template
        context = {
            'full_name': full_name,
            'birth_date': birth_date,
            'phone_number': phone_number,
            'parent_name': parent_name,
            'address': address,
            'group_name': group_obj.name,
            'date_joined': date_joined,
            'client_id': client.id,
        }

        template_dir = os.path.join(settings.BASE_DIR, 'myapp')
        template_path = os.path.join(template_dir, 'templates/client_details_template/client_doc.docx')
        # Загрузка шаблона
        doc = DocxTemplate(template_path)
        # Заполнение шаблона данными
        doc.render(context)
        # Сохранение документа в текущем рабочем каталоге

        saved_file_name = f"{full_name}_{client.id}.docx"
        saved_file_path = os.path.join(template_dir, 'templates/client_details_template', saved_file_name)
        doc.save(saved_file_path)

        # Открытие сохраненного документа
        subprocess.Popen(['start', saved_file_path], shell=True)

        return redirect('client_list')

    groups = Group.objects.all()
    return render(request, 'student_list.html', {'groups': groups})


@login_required
def update_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        client.full_name = request.POST['full_name']
        client.birth_date = request.POST['birth_date']
        client.phone_number = request.POST['phone_number']
        client.parent_name = request.POST['parent_name']
        client.address = request.POST['address']
        client.card_number = request.POST['card_number']
        group_id = request.POST.get('group')
        client.date_joined = request.POST['date_joined']

        group_obj = Group.objects.get(id=group_id)
        client.group_obj = group_obj
        client.save()
        return redirect('client_list')

    groups = Group.objects.all()
    return render(request, 'update_client.html', {'client': client, 'groups': groups})


@login_required
# Удаление клиента
def delete_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return HttpResponseRedirect(reverse('client_list'))




def view_client_profile(request, id):
    client = get_object_or_404(Client, id=id)
    subscriptions = Subscription.objects.filter(client=client)
    markedAttendance = MarkedAttendance.objects.filter(user__client=client)
    clientVisitedDays = [attendance.timestamp.strftime('%Y-%m-%d') for attendance in markedAttendance]

    return render(request, 'client_profile.html', {'client': client, 'subscriptions': subscriptions,
                                                   'markedAttendance': markedAttendance,
                                                   'clientVisitedDays': clientVisitedDays})


@login_required
def add_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        coach_id = request.POST.get('coach')
        description = request.POST.get('description')
        group = Group(
            name=name,
            coach_id=coach_id,
            description=description
        )
        group.save()
        return redirect('group_list')
    else:
        coaches = Coach.objects.all()
    return render(request, 'add_group.html', {'coaches': coaches})


@login_required
def group_list(request):
    groups = Group.objects.all().order_by('coach__full_name')  # Sort by coach's full name
    return render(request, 'group_list.html', {'groups': groups})


@login_required
def update_group(request, id):
    group = Group.objects.get(id=id)
    if request.method == 'POST':
        group.name = request.POST.get('name')
        group.coach_id = request.POST.get('coach')
        group.description = request.POST.get('description')
        group.save()
        return redirect('group_list')
    else:
        coaches = Coach.objects.all()
    return render(request, 'update_group.html', {'group': group, 'coaches': coaches})


@login_required
def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    for client in group.students.all():
        client.group_obj = None
        client.save()
    group.delete()
    return HttpResponseRedirect(reverse('group_list'))


class GroupListView(ListView):
    model = Group
    template_name = 'group_list.html'
    context_object_name = 'groups'


class GroupDetailView(DetailView):
    model = Group
    template_name = 'group_detail.html'
    context_object_name = 'group'

    def generate_report(self, group):
        context = {
            'group': group,
            'clients': [subscription.client for subscription in group.subscription_set.all()]
        }

        template_dir = os.path.join(settings.BASE_DIR, 'myapp')
        template_path = os.path.join(template_dir, 'templates', 'client_details_template', 'group_report_template.docx')

        doc = DocxTemplate(template_path)
        doc.render(context)

        report = io.BytesIO()
        doc.save(report)

        report.seek(0)
        return report


def download_report(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group_detail_view = GroupDetailView()

    report = group_detail_view.generate_report(group)

    response = HttpResponse(report,
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{group.name}_report.docx'

    return response



@login_required
def add_coach(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']
        percent = request.POST['percent']

        coach = Coach(full_name=full_name, phone_number=phone_number, percent=percent)
        coach.save()

        return redirect('coach_list')
    else:
        return render(request, 'add_coach.html')


@login_required
def coach_list(request):
    coaches = Coach.objects.all()
    return render(request, 'coach_list.html', {'coaches': coaches})


@login_required
def update_couch(request, pk):
    coach = get_object_or_404(Coach, id=pk)

    if request.method == 'POST':
        coach.full_name = request.POST['full_name']
        coach.phone_number = request.POST['phone_number']
        coach.percent = request.POST['percent']
        coach.save()

        return redirect('coach_list')
    else:
        return render(request, 'update_couch.html', {'coach': coach})

@login_required
def delete_couch(request, pk):
    coach = get_object_or_404(Coach, id=pk)
    coach.delete()
    return HttpResponseRedirect(reverse('coach_list'))


@login_required
def add_subscription(request):
    if request.method == 'POST':
        group_id = request.POST['group']
        client_id = request.POST['client']
        coach_id = request.POST['coach']
        selected_lesson_schedule = request.POST.get('lesson_schedule', '')
        attendance = request.POST.get('attendance', 'off') == 'on'
        price = request.POST.get('price')
        comment = request.POST['comment']

        group = Group.objects.get(id=group_id)
        client = Client.objects.get(id=client_id)
        coach = Coach.objects.get(id=coach_id)
        selected_lesson_schedule_obj = LessonSchedule.objects.get(id=selected_lesson_schedule)
        lessons_count = selected_lesson_schedule_obj.num_lessons

        subscription = Subscription(group=group, client=client, coach=coach, lessons_count=lessons_count,
                                    attendance=attendance, comment=comment, price=price)
        subscription.save()

        return redirect('subscription_list')
    else:
        groups = Group.objects.all()
        clients = Client.objects.all().order_by('full_name')
        coaches = Coach.objects.all()
        lesson_schedules = LessonSchedule.objects.all()
        return render(request, 'add_subscription.html', {'groups': groups, 'clients': clients,
                                                         'coaches': coaches, 'lesson_schedules': lesson_schedules})







@login_required
def subscription_list(request):

    query = request.GET.get('q')

    if query:
        subscriptions = Subscription.objects.filter(client__full_name__icontains=query)
    else:
        subscriptions = Subscription.objects.all()


    return render(request, 'subscription_list.html', {'subscriptions': subscriptions})


@login_required
def edit_subscription(request, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    lesson_schedules = LessonSchedule.objects.all()

    if request.method == 'POST':
        group_id = request.POST.get('group', '')
        client_id = request.POST.get('client', '')
        coach_id = request.POST.get('coach', '')
        selected_lesson_schedule = request.POST.get('lesson_schedule', '')
        attendance = request.POST.get('attendance', False)
        price = request.POST.get('price', None)  # Получаем стоимость абонемента
        comment = request.POST.get('comment', '')

        selected_lesson_schedule_obj = LessonSchedule.objects.get(id=selected_lesson_schedule)
        lessons_count = selected_lesson_schedule_obj.num_lessons

        subscription.group_id = group_id
        subscription.client_id = client_id
        subscription.coach_id = coach_id
        subscription.lessons_count = lessons_count
        subscription.attendance = attendance == 'on' if isinstance(attendance, str) else attendance
        subscription.price = price
        subscription.comment = comment

        subscription.save()

        return redirect('subscription_list')

    groups = Group.objects.all()
    clients = Client.objects.all()
    coaches = Coach.objects.all()
    price = Subscription.objects.all()
    subscription = Subscription.objects.get(id=subscription_id)
    start_date = subscription.date
    end_date = subscription.end_date

    return render(request, 'edit_subscription.html', {
        'subscription': subscription,
        'groups': groups,
        'clients': clients,
        'coaches': coaches,
        'price': price,
        'subscription': subscription,
        'start_date': start_date,
        'end_date': end_date,
        'lesson_schedules': lesson_schedules
    })


@login_required
def update_subscription(request, subscription_id, action):
    if request.method == 'POST':
        try:
            subscription = Subscription.objects.get(id=subscription_id)

            if action == 'subtract':
                subscription.lessons_count -= 1
                if subscription.lessons_count < 0:
                    subscription.lessons_count = 0
                    subscription.button_highlighted = True

            elif action == 'add':
                subscription.lessons_count += 1
                subscription.button_highlighted = False


            subscription.save()

            # Сохранять информацию об отмеченной посещаемости
            marked_attendance = MarkedAttendance(user=subscription, group=subscription.group)
            marked_attendance.save()

            # Перенаправление на текущую страницу
            return HttpResponseRedirect(reverse(home))
        except Subscription.DoesNotExist:
            return JsonResponse({'error': 'Subscription not found.'}, status=404)

    elif request.method == 'GET':
        try:
            subscription = Subscription.objects.get(id=subscription_id)
            button_highlighted = subscription.button_highlighted
            return JsonResponse({'button_highlighted': button_highlighted})
        except Subscription.DoesNotExist:
            return JsonResponse({'error': 'Subscription not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def delete_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    subscription.delete()
    return HttpResponseRedirect(reverse('client_list'))



@login_required
def check(request):
    subscriptions = Subscription.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        subscriptions = subscriptions.filter(date__range=[start_date, end_date])
        # Вычисляем сумму всех цен подписок за месяц
        total_price = subscriptions.aggregate(total_price=Sum('price'))['total_price']

        return render(request, 'check.html', {'subscriptions': subscriptions,
                                              'total_price': total_price})
    else:
        return render(request, 'check.html', {'subscriptions': subscriptions})





@login_required
def checkcouch(request):
    coach_name = request.GET.get('coach_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date and coach_name:
        coach = get_object_or_404(Coach, full_name=coach_name)
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

        from decimal import Decimal
        paid_subscriptions_total  = Subscription.objects.filter(coach=coach, date__range=(start_datetime, end_datetime), attendance=True).aggregate(total_price=Sum('price'))
        print(paid_subscriptions_total)
        total_price_number = 0
        if paid_subscriptions_total['total_price']:
            total_price_decimal = paid_subscriptions_total['total_price']
            coach_percent = Decimal(coach.percent) / 100
            total_price_number = total_price_decimal * coach_percent




        return render(request, 'checkcouch.html', {'output_message': total_price_number, 'coach_name': coach_name})
    else:
        return render(request, 'checkcouch.html', {'coach_name': coach_name})



def lesson_schedule_list(request):
    lesson_schedules = LessonSchedule.objects.all()
    context = {'lesson_schedules': lesson_schedules}
    return render(request, 'lesson_schedule_list.html', context)


def create_lesson_schedule(request):
    if request.method == 'POST':
        form = LessonScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lesson_schedule_list')
    else:
        form = LessonScheduleForm()

    context = {'form': form}
    return render(request, 'create_lesson_schedule.html', context)


@login_required
def delete_lesson_schedule(request, pk):
    delete_lesson_schedule = get_object_or_404(LessonSchedule, id=pk)

    try:
        with transaction.atomic():
            # # Get the related TrainingRoom object and delete it
            # training_room = delete_lesson_schedule.training_room
            # training_room.delete()

            # Delete all subscriptions related to the LessonSchedule
            subscriptions_to_delete = Subscription.objects.filter(lesson_schedule=delete_lesson_schedule)
            subscriptions_to_delete.delete()

            # Now you can safely delete the LessonSchedule itself
            delete_lesson_schedule.delete()

    except Exception as e:
        print(f"An error occurred: {e}")

    return HttpResponseRedirect(reverse('lesson_schedule_list'))


def edit_lesson_schedule(request, pk):
    lesson_schedule = get_object_or_404(LessonSchedule, id=pk)

    if request.method == 'POST':
        form = LessonScheduleForm(request.POST, instance=lesson_schedule)
        if form.is_valid():
            form.save()
            return redirect('lesson_schedule_list')
    else:
        form = LessonScheduleForm(instance=lesson_schedule)

    context = {'form': form}
    return render(request, 'edit_lesson_schedule.html', context)


def training_room(request):
    if request.method == 'POST':
        form = TrainingRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lesson_schedule_list')  # Перенаправляем на страницу списка учебных планов
    else:
        form = TrainingRoomForm()

    context = {'form': form}
    return render(request, 'training_room.html', context)





