from django.core.management.base import BaseCommand
from requisitions.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Company.objects.all().delete()
        Requisition.objects.all().delete()
        CustomUser.objects.all().delete()