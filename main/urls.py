from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('<str:sign>/', views.fortune, name='fortune'),
    path('about/', views.about, name='about'),
]