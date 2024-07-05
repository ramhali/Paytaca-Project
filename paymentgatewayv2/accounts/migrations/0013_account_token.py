# Generated by Django 5.0.6 on 2024-07-05 03:01

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_remove_account_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='token',
            field=models.CharField(default=accounts.models.Account.generate_token, editable=False, max_length=32, unique=True),
        ),
    ]
