from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.hashers import *
import csv

def index(request):
    context = {}

    return render(request, 'index.html', context)

def register(request):
    context = dict()

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() and form.data['password'] == form.data['password2']:
            user = CustomUser.objects.create_user(username=form.data['username'], password=form.data['password'],
                                                  last_name=form.data['last_name'], first_name=form.data['first_name'])
            user.save()
            context['message'] = 'Вы успешно зарегистрированы!'
            user = authenticate(request, username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')

        elif form.data['password'] != form.data['password2']:
            context['message'] = 'Пароли не совпадают'

    else:
        form = RegisterForm()

    context['users'] = CustomUser.objects.all()
    context['form'] = form
    return render(request, 'register.html', context)

def login_user(request):
    """
        Login page rendering function
        Lets users to login on the website
        :param request: request object
        :return: request answer object, contains *HTML* file
        :rtype: :class: `django.http.HttpResponse`
    """
    context = dict()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                context['message'] = 'Вход выполнен!'
                return HttpResponseRedirect('/')

            context['message'] = 'Не получилось войти:('
    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'login.html', context)

def logout_user(request):
    """
    Logout function
    :param request: request object
    :return: Redirect to login page
    :rtype: :class: `django.http.HttpResponseRedirect`
    """

    logout(request)
    return HttpResponseRedirect('/')

def parser_of_csv(request, table_id):
    context = dict()
    filename = '/home/nippon/Downloads/Test-data.csv'
    a = list()
    #with open(filename, newline='', encoding='cp1251') as file_csv:
    with open(filename) as file_csv:
        file = csv.reader(file_csv)
        for row in file:
            a.append(row)
        print(file)
    context['csvs'] = a
    return render(request, 'table.html', context)
