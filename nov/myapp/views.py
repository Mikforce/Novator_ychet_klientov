from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Coach, Administrator, Subscription, Client
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect

def home(request):
    context = {
        'title': 'Мое приложение учета клиентов'
    }
    return render(request, 'index.html')
# def add_client(request):
#     if request.method == 'POST':
#         full_name = request.POST['full_name']
#         birth_date = request.POST['birth_date']
#         phone_number = request.POST['phone_number']
#         parent_name = request.POST['parent_name']
#
#         date_joined = request.POST['date_joined']
#
#
#         client = Client(full_name=full_name, birth_date=birth_date, phone_number=phone_number,
#                         parent_name=parent_name, date_joined=date_joined)
#         client.save()
#
#         return redirect('client_list')
#     else:
#         groups = Group.objects.all()
#         return render(request, 'student_list.html', {'groups': groups})
#
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})
def add_client(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        birth_date = request.POST['birth_date']
        phone_number = request.POST['phone_number']
        parent_name = request.POST['parent_name']
        group_id = request.POST.get('group')
        date_joined = request.POST['date_joined']

        group_obj = Group.objects.get(id=group_id)
        client = Client(full_name=full_name, birth_date=birth_date, phone_number=phone_number, parent_name=parent_name, group_obj=group_obj, date_joined=date_joined)
        client.save()
        return redirect('client_list')

    groups = Group.objects.all()
    return render(request, 'student_list.html', {'groups': groups})





# Обновление клиента
# def update_client(request, id):
#     client = get_object_or_404(Client, id=id)
#     groupnt = get_object_or_404(Group, id=id)
#
#     if request.method == 'POST':
#         client.full_name = request.POST['full_name']
#         client.birth_date = request.POST['birth_date']
#         client.phone_number = request.POST['phone_number']
#         client.parent_name = request.POST['parent_name']
#         # client.group_obj = request.POST['group_obj']
#         client.date_joined = request.POST['date_joined']
#
#         client.save()
#         return HttpResponseRedirect(reverse('client_list'))
#     else:
#         context = {
#             'client': client,
#         }
#         return render(request, 'update_client.html', context)


def update_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == 'POST':
        client.full_name = request.POST['full_name']
        client.birth_date = request.POST['birth_date']
        client.phone_number = request.POST['phone_number']
        client.parent_name = request.POST['parent_name']
        group_id = request.POST.get('group')
        client.date_joined = request.POST['date_joined']

        group_obj = Group.objects.get(id=group_id)
        client.group_obj = group_obj
        client.save()
        return redirect('client_list')

    groups = Group.objects.all()
    return render(request, 'update_client.html', {'client': client, 'groups': groups})


# Удаление клиента
def delete_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return HttpResponseRedirect(reverse('client_list'))



# def add_group(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         coach_id = request.POST['coach']
#         description = request.POST['description']
#
#         coach = Coach.objects.get(id=coach_id)
#
#         group = Group(name=name, coach=coach, description=description)
#         group.save()
#
#         return redirect('group_list')
#     else:
#         coaches = Coach.objects.all()
#         return render(request, 'add_group.html', {'coaches': coaches})
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
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})



# def update_group(request, id):
#     group = get_object_or_404(Group, id=id)
#     coach = get_object_or_404(Coach, id=id)
#
#     if request.method == 'POST':
#         group.name = request.POST['name']
#         coach.coach_id = request.POST['full_name']
#         group.description = request.POST['description']
#         group.сoach = Coach.objects.get(id=group.coach_id)
#
#         group.save()
#         return HttpResponseRedirect(reverse('group_list'))
#     else:
#         context = {
#             'group': group,
#         }
#         return render(request, 'update_group.html', context)
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

# Удаление клиента
def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    group.delete()
    return HttpResponseRedirect(reverse('group_list'))



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