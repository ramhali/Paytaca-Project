# Generated by Django 5.0.6 on 2024-07-05 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_account_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='token',
        ),
    ]