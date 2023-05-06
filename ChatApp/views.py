from django.shortcuts import render, redirect
from .models import Room, Message
from AppBlog.views import obtener_avatar
from django.contrib.auth.decorators import login_required

@login_required
def buscar_chat(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']
        
        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)

        except Room.DoesNotExist:
            new_room = Room(room_name = room)
            new_room.save()
            return redirect('room', room_name=room, username=username)

    return render(request, 'ChatApp/buscar_chat.html', {"avatar" : obtener_avatar(request)})


@login_required
def chat(request, room_name, username):

    get_room = Room.objects.get(room_name=room_name)

    if request.method == 'POST':
        message = request.POST['message']

        print(message)

        new_message = Message(room=get_room, sender=username, message=message)
        new_message.save()

    get_messages= Message.objects.filter(room=get_room)
    
    context = {"messages": get_messages,"user": username, "avatar" : obtener_avatar(request)}
    return render(request, 'ChatApp/chat.html', context)
