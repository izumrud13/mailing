from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@icloud.com',
            first_name="Admin",
            last_name='Mailing',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('6wL4QmfqtB')
        user.save()