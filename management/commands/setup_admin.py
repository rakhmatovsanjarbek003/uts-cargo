from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Admin foydalanuvchisini xavfsiz yaratish'

    def handle(self, *args, **options):
        User = get_user_model()

        # Ma'lumotlarni o'zgaruvchilardan olish (Xavfsizlik uchun)
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'sanjarbekrahmatov2003@gmail.com')
        password = os.getenv('ADMIN_PASSWORD', 'AD0257857!')
        first_name = 'Sanjarbek'
        last_name = 'Rahmatov'
        phone = '+998944856603'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            self.stdout.write(self.style.SUCCESS(f'Admin "{username}" muvaffaqiyatli yaratildi'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin "{username}" allaqachon mavjud'))