# Generated by Django 3.2.9 on 2022-01-08 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rings', '0009_rating_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='comment',
            field=models.CharField(default='comment placeholder', max_length=2500),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]