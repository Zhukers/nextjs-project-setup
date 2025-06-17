from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Sticker

@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ('preview', 'user', 'city', 'category', 'get_approval_status', 'get_likes_count', 'comments_count', 'created_at')
    list_filter = (
        'approval_status',
        'city',
        'category',
        'created_at',
    )
    search_fields = ('description', 'user__username', 'city__name', 'category__name')
    readonly_fields = ('get_likes_count', 'comments_count', 'views_count', 'created_at', 'updated_at')
    actions = ['approve_stickers', 'reject_stickers', 'export_statistics']
    ordering = ('-created_at',)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        elif obj.video:
            return format_html(
                '<video width="50" height="50" style="border-radius: 4px;"><source src="{}" type="video/mp4"></video>',
                obj.video.url
            )
        return "-"
    preview.short_description = 'Превью'

    def get_approval_status(self, obj):
        status_colors = {
            'pending': '#FFA500',  # Orange
            'approved': '#28A745',  # Green
            'rejected': '#DC3545',  # Red
        }
        status_labels = {
            'pending': 'На модерации',
            'approved': 'Одобрен',
            'rejected': 'Отклонен',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            status_colors.get(obj.approval_status, '#000'),
            status_labels.get(obj.approval_status, obj.approval_status)
        )
    get_approval_status.short_description = 'Статус'

    def get_likes_count(self, obj):
        return obj.total_likes
    get_likes_count.short_description = 'Лайки'

    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Комментарии'

    def approve_stickers(self, request, queryset):
        queryset.update(approval_status='approved')
    approve_stickers.short_description = "Одобрить выбранные стикеры"

    def reject_stickers(self, request, queryset):
        queryset.update(approval_status='rejected')
    reject_stickers.short_description = "Отклонить выбранные стикеры"

    def export_statistics(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stickers_statistics.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Пользователь', 'Город', 'Категория', 
            'Статус', 'Лайки', 'Комментарии', 'Просмотры', 
            'Создан', 'Обновлен'
        ])
        
        for sticker in queryset:
            writer.writerow([
                sticker.id,
                sticker.user.username,
                sticker.city.name,
                sticker.category.name,
                sticker.approval_status,
                sticker.likes.count(),
                sticker.comments.count(),
                sticker.views_count,
                sticker.created_at,
                sticker.updated_at
            ])
        
        return response
    export_statistics.short_description = "Экспортировать статистику"

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'description', 'city', 'category')
        }),
        ('Медиа', {
            'fields': ('image', 'video', 'video_preview', 'aspect_ratio')
        }),
        ('Модерация', {
            'fields': ('approval_status',)
        }),
        ('Статистика', {
            'fields': ('get_likes_count', 'comments_count', 'views_count'),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            total_likes=Count('likes'),
            comments_count=Count('comments')
        )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.approval_status = 'pending'
        super().save_model(request, obj, form, change)
