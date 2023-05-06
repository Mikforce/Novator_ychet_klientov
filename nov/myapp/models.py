from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField('Student', related_name='teachers')
    salary = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    pass_type = models.CharField(max_length=50)
    payment = models.DecimalField(max_digits=8, decimal_places=2)
    start_time = models.DateTimeField()

    def __str__(self):
        return self.name


class Administrator(models.Model):
    name = models.CharField(max_length=100)
    salary_per_hour = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

# Здесь мы определяем три модели: Teacher, Student и Administrator.
#
# Модель Teacher имеет поля name (имя учителя), classes (список классов, которые он ведет) и salary (начисленная зарплата за месяц).
#
# Модель Student имеет поля name (имя ученика), pass_type (тип абонемента), payment (оплата занятий) и start_time (время начала абонемента).
#
# Модель Administrator имеет поля name (имя администратора) и salary_per_hour (зарплата администратора за часы работы).
#
# Также мы используем ManyToManyField в модели Teacher для связи с моделью Student, так как у каждого учителя может быть несколько классов, а у каждого класса может быть несколько учеников.
#
# Это лишь примерный код, который можно доработать и оптимизировать под конкретные потребности студии. Не забудьте запустить миграции после создания моделей, чтобы они были сохранены в базе данных.
