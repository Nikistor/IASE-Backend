import random

from django.core import management
from django.core.management.base import BaseCommand
from requisitions.models import *
from .utils import random_date, random_timedelta


def add_companies():
    Company.objects.create(
        name="Роснефть",
        ticker="ROSN",
        industry="Нефтегаз",
        capital=3206,
        enterprise_value=8170,
        revenue=4988,
        net_profit=181.0,
        pe=17.7,
        ps=0.6,
        pb=1.1,
        ev_ebitda=6.4,
        ebitda_margin=0.3,
        debt_ebitda=3.9,
        report="2016-МСФО",
        year=2016,
        status=1,
        image="companies/1.jpg"
    )

    Company.objects.create(
        name="Газпром",
        ticker="GAZP",
        industry="Нефтегаз",
        capital=2827,
        enterprise_value=4760,
        revenue=6111,
        net_profit=951.6,
        pe=3.0,
        ps=0.5,
        pb=0.2,
        ev_ebitda=3.4,
        ebitda_margin=0.2,
        debt_ebitda=1.4,
        report="2016-МСФО",
        year=2016,
        status=1,
        image="companies/2.jpg"
    )

    Company.objects.create(
        name="Лукойл",
        ticker="LKOH",
        industry="Нефтегаз",
        capital=2299,
        enterprise_value=2736,
        revenue=5227,
        net_profit=206.8,
        pe=11.1,
        ps=0.4,
        pb=0.7,
        ev_ebitda=3.7,
        ebitda_margin=0.1,
        debt_ebitda=0.6,
        report="2016-МСФО",
        year=2016,
        status=1,
        image="companies/3.jpg"
    )

    Company.objects.create(
        name="НОВАТЭК",
        ticker="NVTK",
        industry="Нефтегаз",
        capital=1869,
        enterprise_value=2034,
        revenue=537,
        net_profit=132.5,
        pe=14.1,
        ps=3.5,
        pb=2.8,
        ev_ebitda=8.4,
        ebitda_margin=0.4,
        debt_ebitda=0.7,
        report="2016-МСФО",
        year=2016,
        status=1,
        image="companies/4.jpg"
    )

    Company.objects.create(
        name="ГМК Норникель",
        ticker="GMKN",
        industry="Металургия цвет",
        capital=1237,
        enterprise_value=1513,
        revenue=549,
        net_profit=149.3,
        pe=8.3,
        ps=2.3,
        pb=5.9,
        ev_ebitda=5.9,
        ebitda_margin=0.5,
        debt_ebitda=1.1,
        report="2016-МСФО",
        year=2016,
        status=1,
        image="companies/5.jpg"
    )

    print("Компании добавлены")


def add_requisitions():
    users = CustomUser.objects.filter(is_moderator=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(users) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    companies = Company.objects.all()

    for _ in range(30):
        requisition = Requisition.objects.create()
        requisition.name = "Заявка №" + str(requisition.pk)
        requisition.status = random.randint(2, 5)

        if requisition.status in [3, 4]:
            if requisition.status == 4:
                requisition.date_complete = None
            else:
                requisition.date_complete = random_date()

            if requisition.date_complete:
                requisition.date_formation = requisition.date_complete - random_timedelta()
            else:
                requisition.date_formation = random_date()

            requisition.date_created = requisition.date_formation - random_timedelta()
            requisition.moderator = random.choice(moderators)
            requisition.bankrupt = random.randint(0, 1)
        else:
            requisition.date_formation = random_date()
            requisition.date_created = requisition.date_formation - random_timedelta()

        requisition.employer = random.choice(users)

        for i in range(random.randint(1, 5)):
            requisition.companies.add(random.choice(companies))

        requisition.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_companies()
        add_requisitions()