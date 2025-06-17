from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create test users including a superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Create superuser
        if not User.objects.filter(username='Zhukers').exists():
            User.objects.create_superuser(
                username='Zhukers',
                email='zhurilo1985@gmail.com',
                password='Zhukers_12@'
            )
            self.stdout.write(self.style.SUCCESS('Superuser "Zhukers" created successfully'))
        else:
            self.stdout.write('Superuser "Zhukers" already exists')

        # Create regular test user
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                email='testuser@example.com',
                password='testpass123'
            )
            self.stdout.write(self.style.SUCCESS('Regular user "testuser" created successfully'))
        else:
            self.stdout.write('Regular user "testuser" already exists')
