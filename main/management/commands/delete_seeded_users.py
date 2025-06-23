from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Delete seeded users created during development'

    def handle(self, *args, **kwargs):
        usernames = ['superadmin', 'adminuser', 'limiteduser', 'nopermissionsuser']
        deleted, _ = User.objects.filter(username__in=usernames).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted} user(s)'))
