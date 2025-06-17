from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Sticker(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stickers')
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to='stickers/')
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('cities.City', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField('Доступен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    views_count = models.PositiveIntegerField('Просмотры', default=0)
    likes_count = models.PositiveIntegerField('Лайки', default=0)
    approval_status = models.CharField(
        'Статус модерации',
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending'
    )

    class Meta:
        verbose_name = 'Стикер'
        verbose_name_plural = 'Стикеры'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('stickers:sticker_detail', kwargs={'pk': self.pk})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def toggle_like(self, user):
        like, created = StickerLike.objects.get_or_create(sticker=self, user=user)
        if not created:
            like.delete()
            self.likes_count -= 1
        else:
            self.likes_count += 1
        self.save(update_fields=['likes_count'])
        return created

class StickerLike(models.Model):
    sticker = models.ForeignKey(Sticker, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sticker', 'user')
        verbose_name = 'Лайк стикера'
        verbose_name_plural = 'Лайки стикеров'

    def __str__(self):
        return f'{self.user.username} likes {self.sticker.title}'
