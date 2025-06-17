from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class StickerAdminSite(AdminSite):
    site_title = _('Админ-панель Stickerz')
    site_header = _('Админ-панель Stickerz')
    index_title = _('Управление контентом')

    def get_app_list(self, request, label=None):
        app_list = super().get_app_list(request, label)
        # Reorder the apps
        app_ordering = {
            'stickers': 1,
            'cities': 2,
            'categories': 3,
            'social': 4,
            'notifications': 5,
            'users': 6,
        }
        app_list.sort(key=lambda x: app_ordering.get(x['app_label'], 10))
        return app_list

admin_site = StickerAdminSite(name='admin')

# Register models with the custom admin site
from cities.admin import CityAdmin
from cities.models import City
admin_site.register(City, CityAdmin)

from categories.admin import CategoryAdmin
from categories.models import Category
admin_site.register(Category, CategoryAdmin)

from stickers.admin import StickerAdmin
from stickers.models import Sticker
admin_site.register(Sticker, StickerAdmin)

from notifications.admin import NotificationAdmin
from notifications.models import Notification
admin_site.register(Notification, NotificationAdmin)

from social.admin import LikeAdmin, CommentAdmin
from social.models import Like, Comment
admin_site.register(Like, LikeAdmin)
admin_site.register(Comment, CommentAdmin)

from users.admin import CustomUserAdmin
from users.models import User
admin_site.register(User, CustomUserAdmin)

# Register built-in Django models
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
admin_site.register(Group, GroupAdmin)

from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
admin_site.register(Site, SiteAdmin)
