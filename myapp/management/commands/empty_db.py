from myapp.models import Category, Products, Product_saved
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = "Delete all data from tables"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Product_saved.objects.all().delete()
        Products.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All data from Products and Category has been deleted'))