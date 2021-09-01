from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=200)
    nutriscore = models.IntegerField()
    image_url = models.URLField(max_length=200)
    url_offacts = models.URLField(max_length=200)
    energy_value = models.DecimalField(max_digits=5, decimal_places=1)
    energy_unit = models.CharField(max_length=200)
    sugars_100g = models.DecimalField(max_digits=5, decimal_places=1)
    fat_100g = models.DecimalField(max_digits=5, decimal_places=1)
    saturated_fat_100g = models.DecimalField(max_digits=5, decimal_places=1)
    proteins = models.DecimalField(max_digits=5, decimal_places=1)
    nutriscore_letter_url = models.URLField(max_length=200)
    nutriscore_complete_url = models.URLField(max_length=200)
    categories = models.ManyToManyField(Category,
                                        related_name='product',
                                        blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Product_saved(models.Model):
    product_selected = models.ForeignKey(Products,
                                         related_name='product_selected',
                                         on_delete=models.CASCADE)
    substitution_product = (models
                            .ForeignKey(Products,
                                        related_name='substitution_product',
                                        on_delete=models.CASCADE))
    user = models.ForeignKey(User,
                             related_name='user',
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
