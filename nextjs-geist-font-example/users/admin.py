from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'display_avatar', 'city', 'sticker_count', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'city', 'groups')
    search_fields = ('username', 'email', 'city__name')
    ordering = ('-date_joined',)
    actions = ['activate_users', 'deactivate_users', 'export_user_statistics']

    def display_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 25px;" />',
                obj.avatar.url
            )
        return "-"
    display_avatar.short_description = 'Аватар'

    def sticker_count(self, obj):
        return obj.stickers.count()
    sticker_count.short_description = 'Стикеров'

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Активировать выбранных пользователей"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Деактивировать выбранных пользователей"

    def export_user_statistics(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_statistics.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Username',
            'Email',
            'City',
            'Стикеров',
            'Лайков получено',
            'Комментариев получено',
            'Дата регистрации'
        ])
        
        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.city.name if user.city else '-',
                user.stickers.count(),
                sum(sticker.likes.count() for sticker in user.stickers.all()),
                sum(sticker.comments.count() for sticker in user.stickers.all()),
                user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    export_user_statistics.short_description = "Экспортировать статистику пользователей"

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('email', 'avatar', 'city', 'bio')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('city').prefetch_related(
            'stickers',
            'stickers__likes',
            'stickers__comments'
        )

    list_per_page = 50  # Pagination
