# Generated by Django 5.1.1 on 2024-10-06 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_otpverification_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otpverification',
            name='user',
        ),
    ]
