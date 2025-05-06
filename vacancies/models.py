from datetime import datetime
from django.utils import timezone

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class Company(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    ticker = models.CharField(verbose_name="Тикер", null=True, blank=True)
    industry = models.CharField(verbose_name="Отрасль", null=True, blank=True)
    capital = models.IntegerField(verbose_name="Капитализация (млрд руб)", null=True, blank=True)
    enterprise_value = models.IntegerField(verbose_name="Стоимость компании (млрд руб)", null=True, blank=True)
    revenue = models.IntegerField(verbose_name="Выручка (млрд руб)", null=True, blank=True)
    net_profit = models.FloatField(verbose_name="Чистая прибыль (млрд руб)", null=True, blank=True)
    pe = models.FloatField(verbose_name="P/E", null=True, blank=True)
    ps = models.FloatField(verbose_name="P/S", null=True, blank=True)
    pb = models.FloatField(verbose_name="P/B", null=True, blank=True)
    ev_ebitda = models.FloatField(verbose_name="EV/EBITDA", null=True, blank=True)
    ebitda_margin = models.FloatField(verbose_name="Рентабельность, EBITDA", null=True, blank=True)
    debt_ebitda = models.FloatField(verbose_name="долг/EBITDA", null=True, blank=True)
    report = models.CharField(max_length=255, verbose_name="Отчетность", null=True, blank=True)
    year = models.IntegerField(verbose_name="Год отчетности", null=True, blank=True)

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="companies", default="companies/default.jpg", verbose_name="Фото", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('name', name)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password="1234", **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Vacancy(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    BANKRUPT_CHOICES = (
        (-1, 'Не определён'),
        (0, 'Да'),
        (1, 'Нет')
    )

    bankrupt = models.IntegerField(choices=BANKRUPT_CHOICES, default=-1, verbose_name="Банкрот")

    name = models.CharField(max_length=255, verbose_name="Название")

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    employer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Пользователь", related_name='employer', null=True)
    moderator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Админ", related_name='moderator', blank=True, null=True)

    companies = models.ManyToManyField(Company, verbose_name="Города", null=True)
    report = models.FileField(upload_to='reports/', blank=True, null=True, verbose_name="Отчет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ('-date_formation', )
