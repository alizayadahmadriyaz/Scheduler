


from django.contrib.auth.models import User
# from .models import Message as ChatMessage
from .models import Message as ChatMessage 
from.models import task as Task
from asgiref.sync import sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.users = self.room_name.split("_")[1:]

        if str(self.scope["user"]) not in self.users:
            await self.close()
            return

        self.room_group_name = f"chat_{'_'.join(sorted(self.users))}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Fetch previous messages and send them to user
        await self.send_previous_messages()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_username = data["sender"]
        task_id = None  # Fetch task_id if exists

        receiver_username = [user for user in self.users if user != sender_username][0]

        sender = await sync_to_async(User.objects.get)(username=sender_username)
        receiver = await sync_to_async(User.objects.get)(username=receiver_username)

        if task_id:
            task = await sync_to_async(Task.objects.get)(id=task_id)
        else:
            task = None  # If no task_id is provided, set task to None

        # Save message to database
        await sync_to_async(ChatMessage.objects.create)(
            sender=sender, receiver=receiver, message=message
        )

        # Broadcast message to WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"], "sender": event["sender"]}))

    async def send_previous_messages(self):
        """Fetch previous chat messages and send them when the user connects"""
        messages = await sync_to_async(list)(
            ChatMessage.objects.filter(
                sender__username__in=self.users, receiver__username__in=self.users
            ).order_by("created_at")
        )

        messages_data = [
            {"sender": msg.sender.username, "message": msg.message}
            for msg in messages
        ]

        await self.send(text_data=json.dumps({"previous_messages": messages_data}))
