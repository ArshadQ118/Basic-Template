from django.db import models
from django import forms
from django.contrib.auth.forms import UsernameField, UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, )
    header_image = models.ImageField(upload_to='media/pictures/')
    cover = models.ImageField(upload_to='media/cover/')
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if (created):
        Profile.objects.create(user=instance)
    instance.profile.save()
