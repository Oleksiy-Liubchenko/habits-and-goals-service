# Generated by Django 4.1.7 on 2023-04-12 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_habitdaycompletion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goalstage',
            options={'ordering': ['-status', 'deadline']},
        ),
    ]