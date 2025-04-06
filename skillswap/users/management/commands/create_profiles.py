from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates profiles for existing users who don\'t have one'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        count = 0
        
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} profiles')
        ) 