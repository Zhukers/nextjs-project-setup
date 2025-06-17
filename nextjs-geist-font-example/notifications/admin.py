from django.contrib import admin
from django.utils.html import format_html
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'notification_type', 'is_read', 'created_at', 'sticker_preview')
    list_filter = ('is_read', 'notification_type', 'created_at')
    search_fields = ('recipient__username', 'sender__username', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread']
    ordering = ('-created_at',)

    def sticker_preview(self, obj):
        if obj.sticker and obj.sticker.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.sticker.image.url
            )
        return "-"
    sticker_preview.short_description = 'Стикер'

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Отметить как прочитанное"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Отметить как непрочитанное"

    fieldsets = (
        ('Основная информация', {
            'fields': ('recipient', 'sender', 'notification_type', 'message')
        }),
        ('Связанный контент', {
            'fields': ('sticker',)
        }),
        ('Статус', {
            'fields': ('is_read', 'created_at')
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

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
            status_colors.get(obj.is_read and "approved" or "pending", '#000'),
            status_labels.get(obj.is_read and "approved" or "pending", 'Не прочитано')
        )
    get_approval_status.short_description = 'Статус'

    list_display = ('recipient', 'sender', 'get_approval_status', 'created_at', 'sticker_preview')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'recipient',
            'sender',
            'content_type'
        )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new notification
            obj.is_read = False
        super().save_model(request, obj, form, change)

    list_per_page = 50  # Pagination
