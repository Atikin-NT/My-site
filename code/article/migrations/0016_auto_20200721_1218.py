# Generated by Django 3.0.3 on 2020-07-21 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0015_auto_20200721_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='users/%Y/%m/%d', verbose_name='Аватарка'),
        ),
    ]