# Generated by Django 3.1.4 on 2020-12-22 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20201222_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='header_image',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]
