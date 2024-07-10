from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from accounts.models import Transaction

class Command(BaseCommand):
    help = 'Deletes old MQTT messages from the database.'

    def handle(self, *args, **kwargs):
        older_than = timezone.now() - timedelta(minutes=30)
        Transaction.objects.filter(created_at__lt=older_than, tx_id__isnull=True).delete()
        self.stdout.write(self.style.SUCCESS('Unused MQTT transactions have been deleted.'))
