from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
import uuid

from accounts.models import Token
# Create your views here.

def login(request):
    uid = request.GET.get('token')
    user = auth.authenticate(request, uid=uid)
    if user:
        auth.login(request, user)
    return redirect('/')

def logout(request):
    auth_logout(request)
    return redirect('/')

def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    #print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(reverse('login') + '?token=' + str(token.uid))
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email],)
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    #return render(request, 'login_email_sent.html')
    return redirect('/')
