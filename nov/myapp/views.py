from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Coach, Subscription, Client, Profile, MarkedAttendance
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm
import os
import time
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from .models import UserActivityLog
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Subscription



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

@login_required
def home(request):
    groups = Group.objects.all()
    subscriptions = Subscription.objects.all()
    markedAttendance = MarkedAttendance.objects.all()
    return render(request, 'index.html', {'groups': groups, 'subscriptions': subscriptions, 'markedAttendance': markedAttendance})



@login_required
def users_activity_view(request):
    current_month = datetime.now().month
    users = User.objects.all()
    users_data = []

    for user in users:
        user_activity = UserActivityLog.objects.filter(user=user, timestamp__month=current_month).count()
        users_data.append({
            'user': user,
            'num_activities': user_activity
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
        client = Client(full_name=full_name, birth_date=birth_date, phone_number=phone_number, parent_name=parent_name, address=address, card_number=card_number,
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

        client_details_text = render_to_string('client_details_template/client_details_template.txt', context)

        # Save the client information to a text file
        file_name = f"{slugify(full_name)}_{client.id}_client_details.txt"
        file_path = os.path.join('client_details', file_name)

        # Create the directory if it doesn't exist
        os.makedirs('client_details', exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(client_details_text)
        time.sleep(2)
        # Open the file after saving
        os.system(f'start {file_path}')

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
    groups = Group.objects.all()
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
# Удаление клиента
def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    group.delete()
    return HttpResponseRedirect(reverse('group_list'))


@login_required
def add_coach(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']

        coach = Coach(full_name=full_name, phone_number=phone_number)
        coach.save()

        return redirect('coach_list')
    else:
        return render(request, 'add_coach.html')


@login_required
def coach_list(request):
    coaches = Coach.objects.all()
    return render(request, 'coach_list.html', {'coaches': coaches})


@login_required
def add_subscription(request):
    if request.method == 'POST':
        group_id = request.POST['group']
        client_id = request.POST['client']
        coach_id = request.POST['coach']
        lessons_count = request.POST['lessons_count']
        attendance = request.POST.get('attendance', 'off') == 'on'
        comment = request.POST['comment']

        group = Group.objects.get(id=group_id)
        client = Client.objects.get(id=client_id)
        coach = Coach.objects.get(id=coach_id)

        subscription = Subscription(group=group, client=client, coach=coach, lessons_count=lessons_count,
                                    attendance=attendance, comment=comment)
        subscription.save()

        return redirect('subscription_list')
    else:
        groups = Group.objects.all()
        clients = Client.objects.all()
        coaches = Coach.objects.all()
        return render(request, 'add_subscription.html', {'groups': groups, 'clients': clients, 'coaches': coaches})


@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'subscription_list.html', {'subscriptions': subscriptions})


@login_required
def edit_subscription(request, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)

    if request.method == 'POST':
        group_id = request.POST.get('group', '')
        client_id = request.POST.get('client', '')
        coach_id = request.POST.get('coach', '')
        lessons_count = request.POST.get('lessons_count', '')
        attendance = request.POST.get('attendance', False)
        comment = request.POST.get('comment', '')

        subscription.group_id = group_id
        subscription.client_id = client_id
        subscription.coach_id = coach_id
        subscription.lessons_count = lessons_count
        subscription.attendance = attendance == 'on' if isinstance(attendance, str) else attendance
        subscription.comment = comment

        subscription.save()

        return redirect('subscription_list')

    groups = Group.objects.all()
    clients = Client.objects.all()
    coaches = Coach.objects.all()

    return render(request, 'edit_subscription.html', {
        'subscription': subscription,
        'groups': groups,
        'clients': clients,
        'coaches': coaches
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

            # Save information about the marked attendance
            marked_attendance = MarkedAttendance(user=request.user, group=subscription.group)
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