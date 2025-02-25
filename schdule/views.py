from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import task, Message
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from django.utils.timezone import now
# @login_required
def send_message(request, task_id):
    
    tasks = task.objects.get(id=task_id)
    
    # Assuming the receiver is the owner of the task
    receiver = tasks.user
    sender = request.user

    if sender == receiver:
        messages.error(request, "You cannot send a message to yourself.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect back to task list

    # Create a message
    Message.objects.create(
        sender=sender,
        receiver=receiver,
        # task=tasks,
        message=f"User {sender.username} is interested in traveling from {tasks.departure_place} to {tasks.destination_place}."
    )

    messages.success(request, "Message sent successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # Redirect to the task list page

# @login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid() and not(task.objects.filter(user=request.user).exists()):
            new_task = form.save(commit=False)
            new_task.user = request.user  # Assign the logged-in user
            new_task.save()
            messages.success(request,'Your task created successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.warning(request,'You already have made task')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

def index(request):
    return render(request,'home.html');

def show_all_list(request):
    print(10*'*')
    print(request.user.username)
    print(request.user.username)
    print(now())
    print(10*'*')
    excluded_user = User.objects.get(username=request.user.username)  
    
    if (excluded_user is not None):
        user=request.user

        tasks=task.objects.exclude(user=excluded_user)
        print(task.objects.all())
        return render(request,'all_task.html',{'tasks':tasks})
        
    else:
        messages.warning(request,"First create task")
        return render(request,'alert.html')
    

# def grouping_by_destination(request):

def recieved_message(request):
    filtered_message=messages.objects.filter(receiver=request.user)

    context={"messages":filtered_message}
    return render(request,'message.html',context)


# def grouping(request):



def chat_room(request, user1, user2):
    users = sorted([user1, user2])  # Ensure consistent room naming
    room_name = f"chat_{users[0]}_{users[1]}"
    return render(request, "chat.html", {"room_name": room_name, "other_user": user2})