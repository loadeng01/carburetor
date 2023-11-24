from django.db import models
from apps.category.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()


class Car(models.Model):
    owner = models.ForeignKey(User, related_name='cars', on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    year = models.IntegerField()
    category = models.ForeignKey(Category, related_name='cars', on_delete=models.CASCADE)
    color = models.CharField(max_length=30)
    mileage = models.IntegerField()
    volume = models.DecimalField(max_digits=2, decimal_places=1)
    fuel = models.CharField(max_length=20)
    engine = models.CharField(max_length=10)
    drive_unit = models.CharField(max_length=20)
    kpp = models.CharField(max_length=20)
    str_wheel = models.CharField(max_length=20)
    preview = models.ImageField(upload_to='previews/', blank=True)
    city = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Тачка'
        verbose_name_plural = 'Тачки'


class CarImages(models.Model):
    image = models.ImageField(upload_to='images/')
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)





