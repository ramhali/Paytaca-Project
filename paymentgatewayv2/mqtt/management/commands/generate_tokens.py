import secrets
import string
from django.core.management.base import BaseCommand
from accounts.models import AbstractUser  # Replace with your actual user model

def generate_token(length=32):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for i in range(length))

class Command(BaseCommand):
    help = 'Generate unique tokens for all existing users'

    def handle(self, *args, **kwargs):
        users_without_token = AbstractUser.objects.filter(token__isnull=True)
        for user in users_without_token:
            user.token = generate_token()
            user.save()
