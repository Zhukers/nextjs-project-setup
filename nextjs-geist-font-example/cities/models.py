from django.db import models

class City(models.Model):
    name = models.CharField('Название', max_length=100)
    region = models.CharField('Регион', max_length=100, blank=True)
    country = models.CharField('Страна', max_length=100, default='Россия')
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.region}" if self.region else self.name

    def get_absolute_url(self):
        return f'/cities/{self.id}/'
