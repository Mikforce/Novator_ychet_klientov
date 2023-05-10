from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Coach, Administrator, Subscription, Client
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy


from django.shortcuts import render, redirect


def add_client(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        birth_date = request.POST['birth_date']
        phone_number = request.POST['phone_number']
        parent_name = request.POST['parent_name']

        date_joined = request.POST['date_joined']


        client = Client(full_name=full_name, birth_date=birth_date, phone_number=phone_number,
                        parent_name=parent_name, date_joined=date_joined)
        client.save()

        return redirect('client_list')
    else:
        groups = Group.objects.all()
        return render(request, 'student_list.html', {'groups': groups})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def edit_delete_client(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client = Client.objects.get(id=client_id)

        if 'edit' in request.POST:
            # Выполнить действия для редактирования клиента
            return render(request, 'client_edit.html', {'client': client})
        elif 'delete' in request.POST:
            # Выполнить действия для удаления клиента
            client.delete()
            return redirect('client_list')




def add_group(request):
    if request.method == 'POST':
        name = request.POST['name']
        coach_id = request.POST['coach']
        description = request.POST['description']

        coach = Coach.objects.get(id=coach_id)

        group = Group(name=name, coach=coach, description=description)
        group.save()

        return redirect('group_list')
    else:
        coaches = Coach.objects.all()
        return render(request, 'add_group.html', {'coaches': coaches})

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})



from django.shortcuts import render, redirect
from .models import Coach

def add_coach(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']

        coach = Coach(full_name=full_name, phone_number=phone_number)
        coach.save()

        return redirect('coach_list')
    else:
        return render(request, 'add_coach.html')

def coach_list(request):
    coaches = Coach.objects.all()
    return render(request, 'coach_list.html', {'coaches': coaches})




def add_admin(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']

        admin = Administrator(full_name=full_name, phone_number=phone_number)
        admin.save()

        return redirect('admin_list')
    else:
        return render(request, 'add_admin.html')

def admin_list(request):
    admins = Administrator.objects.all()
    return render(request, 'admin_list.html', {'admins': admins})




def add_subscription(request):
    if request.method == 'POST':
        group_id = request.POST['group']
        client_id = request.POST['client']
        coach_id = request.POST['coach']
        lessons_count = request.POST['lessons_count']
        attendance = request.POST.get('attendance', False)
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

def subscription_list(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'subscription_list.html', {'subscriptions': subscriptions})