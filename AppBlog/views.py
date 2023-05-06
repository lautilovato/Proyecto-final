from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import *
from .models import Blog, Avatar
from django.contrib.auth.decorators import login_required




def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            info=form.cleaned_data
            
            usu=info["username"]
            clave=info["password"]
            usuario=authenticate(username=usu, password=clave)#verifica si el usuario existe, si existe, lo devuelve, y si no devuelve None 
            
            if usuario is not None:
                login(request, usuario)
                blogs = Blog.objects.all()
                contexto = {"blogs" : blogs, "avatar" : obtener_avatar(request)}
                return render(request, "AppBlog/inicio.html", contexto)
            else:
                return render(request, "AppBlog/formL.html", {"form": form, "avatar" : obtener_avatar(request)})
        else:
            return render(request, "AppBlog/formL.html", {"form": form, "avatar" : obtener_avatar(request)})
    else:
        form=AuthenticationForm()
        return render(request, "AppBlog/formL.html", {"form": form, "avatar" : obtener_avatar(request)})

def register(request):
    if request.method=="POST":
        form= RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            blogs = Blog.objects.all()
            contexto = {"blogs" : blogs,"avatar" : obtener_avatar(request)}
            return render(request, "AppBlog/inicio.html", contexto)
        else:
            return render(request, "AppBlog/formR.html", {"form": form})
    else:
        form= RegistroUsuarioForm()
        return render(request, "AppBlog/formR.html", {"form": form})

@login_required
def perfil_detalle(request):
    return render(request, "AppBlog/perfil.html", {"avatar" : obtener_avatar(request)})

@login_required
def editar_perfil(request):
    usuario=request.user

    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():

            info=form.cleaned_data
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password2"]
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.perfil.web_link=info["web_link"]
            usuario.perfil.descripcion=info["descripcion"]
            usuario.save()

            blogs = Blog.objects.all()
            contexto = {"blogs" : blogs, "avatar" : obtener_avatar(request)}
            return render(request, "AppBlog/inicio.html", contexto)
        else:
            return render(request, "AppBlog/editar_perfil.html", {"form": form, "nombreusuario":usuario.username, "avatar" : obtener_avatar(request)})
    else:
        form=UserEditForm(instance=usuario)
        return render(request, "AppBlog/editar_perfil.html", {"form": form, "nombreusuario":usuario.username, "avatar" : obtener_avatar(request)})

@login_required      
def inicio(request):
    blogs = Blog.objects.all()
    contexto = {"blogs" : blogs, "avatar" : obtener_avatar(request)}
    return render(request, "AppBlog/inicio.html", contexto)

@login_required 
def agregar_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = Blog()
            blog.imagen = form.cleaned_data["imagen"]
            blog.titulo = form.cleaned_data["titulo"]
            blog.subtitulo = form.cleaned_data["subtitulo"]
            blog.cuerpo = form.cleaned_data["cuerpo"]
            blog.autor = form.cleaned_data["autor"]
            blog.fecha = form.cleaned_data["fecha"]
            blog.save()
            form = BlogForm()
    else:
            form = BlogForm()
    
    contexto = { "form" : form, "avatar" : obtener_avatar(request)}
    return render(request, "AppBlog/agregar_blog.html", contexto)
@login_required 
def blog(request, id):
    blog= Blog.objects.get(id= id)
    contexto= {'blog' : blog, "avatar" : obtener_avatar(request)}
    return render(request, "AppBlog/blog.html", contexto)

@login_required 
def eliminar_blog(request, id):
    blog=Blog.objects.get(id=id)
    print(blog)
    blog.delete()
    blogs=Blog.objects.all()
    form = BlogForm()
    return render(request, "AppBlog/inicio.html", {"blogs" : blogs, "form": form, "avatar" : obtener_avatar(request)})

@login_required 
def editar_blog(request, id):
    blog=Blog.objects.get(id=id)
    if request.method=="POST":
        form= BlogForm(request.POST, request.FILES)
        if form.is_valid():
            
            info=form.cleaned_data
            
            blog.imagen=info["imagen"]
            blog.titulo=info["titulo"]
            blog.subtitulo=info["subtitulo"]
            blog.cuerpo=info["cuerpo"]
            blog.autor=info["autor"]
            blog.fecha=info["fecha"]
            
            blog.save()
            blogs=Blog.objects.all()
            form = BlogForm()
            return render(request, "AppBlog/inicio.html" ,{"blogs" : blogs, "form" : form, "avatar" : obtener_avatar(request)})
    else:
        form= BlogForm(initial={"imagen":blog.imagen, "titulo":blog.titulo, "subtitulo":blog.subtitulo, "cuerpo":blog.cuerpo, "autor":blog.autor, "fecha":blog.fecha})
    return render(request, "AppBlog/editar_blog.html", {"form": form, "blog": blog, "avatar" : obtener_avatar(request)})

@login_required     
def obtener_avatar(request):
    avatares=Avatar.objects.filter(user=request.user.id)
    if len(avatares)!=0:
        return avatares[0].imagen.url
    else:
        return "/media/avatars/avatar_default.jpg"

@login_required 
def agregar_avatar(request):
    if request.method=="POST":
        form=AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar=Avatar(user=request.user, imagen=request.FILES["imagen"])#antes de guardarlo, tengo q hacer algo
            
            avatarViejo=Avatar.objects.filter(user=request.user)
            if len(avatarViejo)>0:
                avatarViejo[0].delete()
            avatar.save()
            blogs=Blog.objects.all()
            return render(request, "AppBlog/inicio.html", {"mensaje":f"Avatar agregado correctamente", "avatar":obtener_avatar(request), "blogs" : blogs})
        else:
            return render(request, "AppBlog/agregar_avatar.html", {"form": form, "usuario": request.user, "mensaje":"Error al agregar el avatar"})
    else:
        form=AvatarForm()
        return render(request, "AppBlog/agregar_avatar.html", {"form": form, "usuario": request.user, "avatar":obtener_avatar(request)})

@login_required     
def about(request):
    contexto = { "avatar" : obtener_avatar(request)}
    return render(request, "AppBlog/about.html", contexto)    