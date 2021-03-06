# Generated by Django 3.2.5 on 2022-02-25 05:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_bookedday'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedday',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookedday',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
