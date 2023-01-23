from django.shortcuts import render, redirect
from django.http import HttpResponse
from project.models import *
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import smtplib
import requests
import random
import math


def home(request):
    data = {}
    if not request.session.get('username'):
        request.session['username'] = ''
    return render(request, 'index.html', data)


def register(request):
    data = {}
    username = request.session['username']
    users = User.objects.all()
    for user in users:
        if user.username == username:
            break
    if user.is_admin == 1:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            company = request.POST.get('company')
            is_admin = request.POST.get('is_admin')
            user = User.objects.filter(username=username)
            if user:
                data['msg'] = "User already exist!"
            else:
                newuser = User.objects.create(username=username,
                                              password=password,
                                              email=email,
                                              phone=phone,
                                              company=company,
                                              is_admin=is_admin)
                newuser.save()
                data['msg'] = "User " + username + " created."
    else:
        data['msg'] = "You do not have access to register. Only admin can do it."
        return render(request, 'index.html', data)
    return render(request, 'register.html', data)


def login(request):
    data = {}
    username = request.session['username']
    if username != '':
        data['msg'] = "User " + username + " has logged in already!"
        return render(request, 'index.html', data)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            users = User.objects.all()
            for user in users:
                if user.username == username:
                    if user.password == password:
                        request.session['username'] = username
                        request.session['isadmin'] = user.is_admin
                        data['msg'] = "User " + username + " logged in."
                        return render(request, 'index.html', data)
                    else:
                        data['msg'] = "Wrong password!"
                    break
            else:
                data['msg'] = "User does not exist!"
    return render(request, 'login.html', data)


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def sendOTP(request):
    username = request.POST.get("un")
    user = User.objects.get(username=username)
    if user:
        OTP = generateOTP()

        email_sender = 'riaduttademo@gmail.com'
        email_password = 'wokvndvsrmufesgz'
        email_receiver = user.email

        subject = 'Reset Password'
        body = "The OTP for reseting your password is " + OTP

        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.login(email_sender, email_password)
        s.sendmail(email_sender, email_receiver, body)
        s.quit()

        return HttpResponse(OTP)
    else:
        return HttpResponse(-1)


def confirmOTP(request):
    otp = request.POST.get("otp")
    otp_gen = request.POST.get("otp_gen")
    if otp == otp_gen:
        return HttpResponse(1)
    else:
        return HttpResponse(0)


def passwordChanged(request):
    username = request.POST.get('un')
    newpass = request.POST.get('newpass')
    print(username)
    print(newpass)
    user = User.objects.get(username=username)
    user.password = newpass
    user.save()
    return HttpResponse(1)


def forgotpassword(request):
    data = {}
    return render(request, 'forgot-password.html', data)


def logout(request):
    data = {}
    username = request.session['username']
    if username == '':
        data['msg'] = "No one has logged in!"
    else:
        data['msg'] = "User " + username + " logged out."
        request.session['username'] = ''
        request.session['isadmin'] = 0
    return render(request, 'index.html', data)


def createproject(request):
    data = {}
    username = request.session['username']
    if username == '':
        data['msg'] = "No one has logged in!"
        return render(request, 'index.html', data)
    else:
        if request.method == 'POST':
            pname = request.POST.get('pname')
            description = request.POST.get('description')
            stype = request.POST.get('stype')
            accessed = request.POST.get('accessed')
            user = User.objects.get(username=username)
            newproject = Project.objects.create(pname=pname,
                                                description=description,
                                                service_type=stype,
                                                accessed=accessed,
                                                created_by=user)
            newproject.save()
            data['msg'] = "New project '" + pname + "' created."
    return render(request, 'create-project.html', data)


def allprojects(request):
    data = {}
    projects = Project.objects.filter(accessed='public')
    data['projects'] = projects
    return render(request, 'all-projects.html', data)


def myprojects(request):
    data = {}
    username = request.session['username']
    user = User.objects.get(username=username)
    projects = Project.objects.filter(created_by=user)
    data['projects'] = projects
    return render(request, 'my-projects.html', data)


def project(request, id):
    data = {}
    projects = Project.objects.all()
    for project in projects:
        if project.id == id:
            break
    data['project'] = project
    return render(request, 'project.html', data)
