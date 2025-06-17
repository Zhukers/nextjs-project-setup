from django.contrib import admin
from django.utils.html import format_html
from .models import Like, Comment

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'sticker_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'sticker__description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def sticker_preview(self, obj):
        if obj.sticker.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.sticker.image.url
            )
        return "-"
    sticker_preview.short_description = 'Стикер'

    fieldsets = (
        ('Информация о лайке', {
            'fields': ('user', 'sticker', 'created_at')
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'sticker_preview', 'text_preview', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'text', 'sticker__description')
    readonly_fields = ('created_at',)
    actions = ['approve_comments', 'reject_comments']
    ordering = ('-created_at',)

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст'

    def sticker_preview(self, obj):
        if obj.sticker.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.sticker.image.url
            )
        return "-"
    sticker_preview.short_description = 'Стикер'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Одобрить выбранные комментарии"

    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
    reject_comments.short_description = "Отклонить выбранные комментарии"

    fieldsets = (
        ('Информация о комментарии', {
            'fields': ('user', 'sticker', 'text')
        }),
        ('Модерация', {
            'fields': ('is_approved', 'created_at')
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new comment
            obj.is_approved = False
        super().save_model(request, obj, form, change)

    list_per_page = 50  # Pagination
