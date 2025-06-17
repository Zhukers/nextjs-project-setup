from django.contrib import admin
from django.utils.html import format_html
from .models import City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'sticker_count', 'user_count')
    list_filter = ('region',)
    search_fields = ('name', 'region')
    readonly_fields = ('sticker_count', 'user_count')
    actions = ['export_as_csv']

    # Removed display_image method because City model has no image field
    # def display_image(self, obj):
    #     if obj.image:
    #         return format_html('<img src="{}" width="50" height="50" style="border-radius: 4px;" />', obj.image.url)
    #     return "-"
    # display_image.short_description = 'Изображение'

    def sticker_count(self, obj):
        return obj.sticker_set.count()
    sticker_count.short_description = 'Стикеров'

    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'Пользователей'

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cities.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Название', 'Регион', 'Количество стикеров', 'Количество пользователей'])
        
        for city in queryset:
            writer.writerow([
                city.name,
                city.region,
                city.sticker_set.count(),
                city.user_set.count()
            ])
        
        return response
    export_as_csv.short_description = "Экспортировать выбранные города в CSV"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'region')
        }),
        ('Статистика', {
            'fields': ('sticker_count', 'user_count'),
            'classes': ('collapse',)
        }),
        ('Геолокация', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
    )
