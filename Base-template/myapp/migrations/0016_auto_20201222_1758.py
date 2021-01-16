# Generated by Django 3.1.4 on 2020-12-22 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_auto_20201222_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cover',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='media/cover/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='header_image',
            field=models.ImageField(upload_to='media/pictures/'),
        ),
    ]
