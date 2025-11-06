from django.urls import path
from . import views

app_name = 'skinsense'  # <--- IMPORTANT

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about_page, name='about'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('followup/', views.followup_page, name='followup'),
    path('logout/', views.logout_user, name='logout'),
]