# Generated by Django 3.2.9 on 2021-12-29 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Rings', '0004_auto_20211213_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ring',
            name='user',
        ),
    ]
