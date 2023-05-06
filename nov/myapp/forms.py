from django import forms
from .models import Student, Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'pass_type', 'payment', 'start_time']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('name', 'classes', 'salary')