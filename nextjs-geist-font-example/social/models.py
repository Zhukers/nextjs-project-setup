from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class UserFollow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Подписчик')
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=_('Подписан на')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата подписки')
    )

    class Meta:
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки')
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"

class UserMessage(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name=_('Отправитель')
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name=_('Получатель')
    )
    text = models.TextField(
        max_length=1000,
        verbose_name=_('Текст сообщения'),
        default=''
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата отправки')
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Прочитано')
    )

    class Meta:
        verbose_name = _('Сообщение')
        verbose_name_plural = _('Сообщения')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.text[:50]}"

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name=_('Пользователь')
    )
    sticker = models.ForeignKey(
        'stickers.Sticker',
        on_delete=models.CASCADE,
        related_name='social_likes',
        verbose_name=_('Стикер')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    class Meta:
        verbose_name = _('Лайк')
        verbose_name_plural = _('Лайки')
        unique_together = ('user', 'sticker')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.sticker.id}"

class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Пользователь')
    )
    sticker = models.ForeignKey(
        'stickers.Sticker',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Стикер')
    )
    text = models.TextField(
        max_length=500,
        verbose_name=_('Текст')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_('Одобрен')
    )

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.text[:50]}"
