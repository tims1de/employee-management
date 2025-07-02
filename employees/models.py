import datetime

from django.contrib.auth.models import Group, User
from django.db import models


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, editable=False, verbose_name="Аккаунт пользователя")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=100, verbose_name="Должность")
    employment_date = models.DateField(verbose_name="Дата приёма на работу")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")
    total_paid = models.DecimalField(editable=False, max_digits=15, decimal_places=2,verbose_name="Общая сумма выплат")
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,verbose_name="Начальник")
    level = models.PositiveIntegerField(verbose_name="Уровень")

    def save(self, *args, **kwargs):
        months = self.calculate_paid_months(self.employment_date)
        self.total_paid = self.salary * months
        creating = self.pk is None  # Новый объект или нет

        super().save(*args, **kwargs)  # Первый save нужен, чтобы получить self.id

        if creating and not self.user:
            username = f"user_{self.position}_{self.id}".lower().replace(' ', '_')
            first_name = self.full_name.split()[0] if self.full_name else ''
            last_name = ' '.join(self.full_name.split()[1:]) if self.full_name else ''

            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_staff=True
            )

            user.set_unusable_password()
            user.save()

            try:
                group = Group.objects.get(name=self.position)
                user.groups.add(group)
            except Group.DoesNotExist:
                print(f"Группа с именем '{self.position}' не найдена! Создай её в Django Admin.")

            self.user = user
            super().save(update_fields=['user'])

    @staticmethod
    def calculate_paid_months(start_data):
        current_date = datetime.date.today()
        delta = current_date - start_data
        months = delta.days // 30
        return months

    class Meta:
        verbose_name = "Работники"
        verbose_name_plural = "Работники"

    def __str__(self):
        return self.full_name

