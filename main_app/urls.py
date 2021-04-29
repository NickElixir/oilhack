from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('reg/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]