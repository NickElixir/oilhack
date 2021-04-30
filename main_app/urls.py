from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('reg/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('<int:table_id>/', views.parser_of_csv, name='table'),
    path('search_results/',views.search_results, name='search_results'),
    #path('test/', views.parser_of_csv, name='table'),
]
