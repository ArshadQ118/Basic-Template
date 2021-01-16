from django.http import request
from django.http.response import HttpResponseRedirect
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.urls.base import reverse
from django.utils.encoding import force_text
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connections
import mysql.connector
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.template.loader import render_to_string
from .forms import SignUpForm
from django.db import IntegrityError
from operator import itemgetter
from django.contrib.auth.forms import UserCreationForm, forms
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
import smtplib
from .models import Profile
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404


def HomeView(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')


def activation_sent(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return render(request, 'home.html')
    else:
        return HttpResponse('activation_invalid')


def registration(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already Registered!")
        return render(request, 'home.html')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.profile.email = form.cleaned_data.get('email')
                user.profile.header_image = form.cleaned_data.get('header_image')
                user.profile.cover = form.cleaned_data.get('cover')
                user.is_active = False
                user.save()
                messages.success(request, 'Your Data has been Accepted!')
                current_site = get_current_site(request)
                subject = 'Please Activate Your Account'
                message = render_to_string('activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(subject, message, to=[to_email])
                email.send()
                return render(request, 'activation_sent.html')
            else:
                messages.warning(request, 'Credentials Invalid Please Try Again!.')
        else:
            form = SignUpForm()
        return render(request, 'register.html', {'form': form})


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contacts = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contacts.save()
        messages.success(request, 'Your messages has been Send!')
    return render(request, 'contact.html')


def loginUser(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return render(request, 'home.html')
    else:

        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return render(request, 'home.html')
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                messages.warning(request, 'Credentials Invalid Please Try Again!.')
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(
                    username, password))
                return render(request, 'login.html')

        else:
            # Nothing has been provided for username or password.
            return render(request, 'login.html', {})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('/login')


def password_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Change Successfully')
                return HttpResponseRedirect('/home/')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'password_change_form.html', {'form': form})
    else:
        return HttpResponseRedirect('/home/')


# class CreateImage(CreateView):
#     model = Profile
#     form_class = PostForm
#     template_name = 'register.html'
#     success_url = reverse_lazy('home')

def profile(request):
    return render(request, 'profile.html')
