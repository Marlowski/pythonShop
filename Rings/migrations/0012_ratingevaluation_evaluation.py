# Generated by Django 3.2.9 on 2022-01-08 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rings', '0011_ratingevaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingevaluation',
            name='evaluation',
            field=models.CharField(choices=[('POS', 'helpful'), ('NEG', 'not helpful'), ('REP', 'reported')], default='POS', max_length=3),
            preserve_default=False,
        ),
    ]
