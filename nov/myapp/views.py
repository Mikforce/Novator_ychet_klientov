from django.shortcuts import render, redirect
from .models import Teacher, Student, Administrator
from .forms import StudentForm, TeacherForm

def teacher_list(request):

    teachers = Teacher.objects.all()
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'add_teacher.html', {'form': form})

    return render(request, 'base.html', {'teachers': teachers})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def administrator(request):
    lessons = Administrator.objects.all()
    return render(request, 'lesson_list.html', {'lessons': lessons})

def add_lesson(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lesson_list')
    else:
        form = StudentForm()
    return render(request, 'add_lesson.html', {'form': form})