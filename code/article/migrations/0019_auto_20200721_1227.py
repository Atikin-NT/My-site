# Generated by Django 3.0.3 on 2020-07-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0018_auto_20200721_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='users/', verbose_name='Аватарка'),
        ),
    ]