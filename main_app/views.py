from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.hashers import *
import re
import pandas as pd
from django.conf import settings
from django.conf.urls.static import static
import csv
import numpy as np
import matplotlib.pyplot as plt

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

links_table = pd.read_csv('TGB/propertys/links_table.csv', sep=';')
word = 'ГПН'
returnable_df = pd.DataFrame()
index_comp = links_table.loc[links_table.company_name == word]['id-company'].iloc[0]
for i in [5, 6]:
    path = "media/1.csv"
    tmp = pd.read_csv(path, sep=';')
    returnable_df = returnable_df.append(tmp)

def get_hist(returnable_df):
    labels = returnable_df['Наименование компонента'].values
    x1 = returnable_df['Бюджет'] / returnable_df['Бюджет'].sum()
    print(x1)
    x2 = returnable_df['Доля в проекте'] / returnable_df['Доля в проекте'].sum()

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(16, 12))
    rects1 = ax.bar(x - width / 2, x1, width, label='Бюджет')
    rects2 = ax.bar(x + width / 2, x2, width, label='Доля в проекте')

    # Add some text for labels, title and custom x-axis tick labels, etc.

    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.xticks(rotation=90)
    fig.tight_layout()
    fig.savefig('media/Testfig.png')

def parser_of_csv(request, table_id):
    get_hist(returnable_df)
    context = dict()
    filename = settings.MEDIA_ROOT + '/'  + str(table_id) + '.csv'
    a = list()
    with open(filename, newline='', encoding='utf-8') as file_csv:
        file = csv.reader(file_csv)
        for row in file:
            a.append(row[0].split(';'))
    context['img'] = 'Testfig.png'
    context['csv'] = a
    context['fileurl'] = settings.MEDIA_ROOT + '/' + str(table_id) + '.csv'
    return render(request, 'table.html', context)

@login_required(login_url='/login')
def search_results(request):
    context = {}
    context['user_name'] = request.user
    if 'search-btn' and 'search-line' in request.GET:
        s_line = request.GET['search-line']
        try:
            companies = []
            for company in Company.objects.all():
                if re.search(r'{}'.format(s_line), company.name):
                    companies.append(company)
                    print(company)
        except:
            companies = Company.objects.filter(name__startswith=s_line)
        context['search_value'] = s_line
        context['companies_on_search'] = companies
    return render(request, 'search_results.html', context)
