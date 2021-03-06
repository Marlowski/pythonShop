# Generated by Django 3.2.9 on 2022-01-03 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cart', '0004_auto_20211231_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='user_type',
        ),
        migrations.AddField(
            model_name='payment',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='items',
            field=models.CharField(default='ff', max_length=3000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='user_elem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
