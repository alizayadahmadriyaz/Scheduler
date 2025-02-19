from django.urls import path
from .views import create_task,index,show_all_list,send_message,chat_room

urlpatterns = [
    path('create-task/', create_task, name='create_task'),
    path('index/', index, name='home'),
    path('all_list/',show_all_list,name="listing"),
    path('send_message/<int:task_id>/', send_message, name='send_message'),
    path("chat/<str:user1>/<str:user2>/", chat_room, name="chat_room"),
]
