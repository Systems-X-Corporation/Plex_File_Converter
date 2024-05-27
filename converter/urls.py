from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'converter'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.MainView.as_view(), name='upload_file'),
    #path('working', views.upload_file, name='upload_file'),

]