from django.urls import path
from .views import *

urlpatterns = [
    path('', buscar_chat, name='buscar_chat'),
    path('<str:room_name>/<str:username>/', chat, name='room'),
]