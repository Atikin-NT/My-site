# Generated by Django 3.0.3 on 2020-04-15 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20200411_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='coding',
            field=models.BooleanField(default=0, verbose_name='Категория кодинг'),
        ),
    ]
