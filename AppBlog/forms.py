from django import forms
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.models import User
from django.db import models

class RegistroUsuarioForm(UserCreationForm):
    email=forms.EmailField(label="Email")
    password1=forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta: # clase de configuracion
        model=User
        fields=["username", "email", "password1", "password2"]
        help_texts = {k:"" for k in fields}

class BlogForm(forms.Form):
    
    imagen= forms.ImageField(label="imagen")
    titulo= forms.CharField(max_length= 100)
    subtitulo= forms.CharField(max_length= 1000)
    cuerpo= forms.CharField(max_length= 99999)
    autor= forms.CharField(max_length= 50)
    fecha= forms.DateField()

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)


        self.fields['imagen'].widget.attrs.update({'class': 'form-control'})
        self.fields['subtitulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['titulo'].widget.attrs.update({'class': 'form-control'})
        self.fields['cuerpo'].widget.attrs.update({'class': 'form-control'})
        self.fields['autor'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha'].widget.attrs.update({'class': 'form-control'})

        
class UserEditForm(UserCreationForm):
    email= forms.EmailField(label= "Email")
    password1= forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2= forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    first_name= forms.CharField(label="Modificar Nombre")
    last_name= forms.CharField(label="Modificar Apellido")
    web_link= forms.CharField(label="Modificar link")
    descripcion= forms.CharField(label="Modificar Descripción")

    class Meta:
        model=User
        fields=["email", "password1", "password2", "first_name", "last_name"]
        help_texts = {k:"" for k in fields}#para cada uno de los campos del formulario, le asigna un valor vacio


class AvatarForm(forms.Form):
    imagen = forms.ImageField(label= "imagen")

