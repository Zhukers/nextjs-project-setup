from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='user_avatars/',
        null=True,
        blank=True,
        verbose_name=_('Аватар')
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_('О себе')
    )
    city = models.ForeignKey(
        'cities.City',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_set',
        verbose_name=_('Город')
    )
    
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def get_sticker_count(self):
        return self.sticker_set.count()
    get_sticker_count.short_description = _('Количество стикеров')

    def get_likes_received(self):
        return sum(sticker.likes.count() for sticker in self.sticker_set.all())
    get_likes_received.short_description = _('Полученные лайки')

    def get_comments_received(self):
        return sum(sticker.comments.count() for sticker in self.sticker_set.all())
    get_comments_received.short_description = _('Полученные комментарии')
