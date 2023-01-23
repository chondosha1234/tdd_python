from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
import uuid
import sys

from accounts.models import Token
# Create your views here.

def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(request, uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')

def logout(request):
    auth_logout(request)
    return redirect('/')

def send_login_email(request):
    email = request.POST['email']
    #uid = str(uuid.uuid4())
    #Token.objects.create(email=email, uid=uid)
    #print('saving uid', uid, 'for email', email, file=sys.stderr)
    #url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for Superlists',
        'body text tbc',
        'noreply@superlists',
        [email],)
    #return render(request, 'login_email_sent.html')
    return redirect('/')
