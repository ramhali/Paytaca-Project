# Generated by Django 5.0.6 on 2024-07-10 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_transaction_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='status',
        ),
        migrations.AddField(
            model_name='transaction',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
