# Generated by Django 3.2.25 on 2024-05-08 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_reservation_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='exam_slot',
            new_name='exam',
        ),
    ]
