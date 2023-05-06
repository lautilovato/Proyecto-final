from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', register, name="register"),
    path('login_request/',login_request, name="login_request"),
    path('logout/', LogoutView.as_view(), name= "logout"), 
    path('inicio/', inicio, name="inicio"),
    path('agregar_blog/', agregar_blog, name="agregar_blog"),
    path('blog/<id>', views.blog, name="blog"),
    path('eliminar_blog/<id>', eliminar_blog, name="eliminar_blog"),
    path('editar_blog/<id>', editar_blog, name="editar_blog"),
    path('editar_perfil/', editar_perfil, name="editar_perfil"),
    path('perfil_detalle', perfil_detalle, name="perfil_detalle"),
    path('agregar_avatar/', agregar_avatar, name= "agregar_avatar" ),
    path('about/', about, name="about"),
]