# Generated by Django 3.1.4 on 2020-12-21 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20201221_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='img.jpg', upload_to='UserProfile'),
        ),
    ]
