from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Blog(models.Model):
    imagen= models.ImageField(upload_to="imagenes")
    titulo= models.CharField(max_length= 100)
    subtitulo= models.CharField(max_length= 1000)
    cuerpo= models.CharField(max_length= 99999)
    autor= models.CharField(max_length= 50)
    fecha= models.DateField()
    def __str__(self):
        return f"{self.titulo}"

class Avatar(models.Model):
    imagen= models.ImageField(upload_to="avatars")
    user=models.ForeignKey(User, on_delete=models.CASCADE)  

class Perfil(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    descripcion= models.CharField(max_length= 500, null= True, blank= True)
    web_link= models.CharField(max_length= 500, null= True, blank= True)

    class Meta:
        verbose_name= "Perfil"
        verbose_name_plural="Perfiles"
        ordering= ["-id"]

def create_user_perfil(sender, instance, created, **kwargs):
	if created:
		Perfil.objects.create(user=instance)

def save_user_perfil(sender, instance, **kwargs):
	instance.perfil.save()

post_save.connect(create_user_perfil, sender=User)
post_save.connect(save_user_perfil, sender=User)