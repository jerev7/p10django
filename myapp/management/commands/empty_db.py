from myapp.models import Category, Products
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = "Delete all data from tables"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Products.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All data from Products and Category has been deleted'))