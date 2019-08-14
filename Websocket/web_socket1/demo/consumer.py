from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from demo.views import send_static_emition, sned_interact_static, send_stranger_static, send_fall_static, \
    send_attack_static


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        if self.room_name == "emotion":
            send_static_emition()

        if self.room_name == "interact":
            sned_interact_static()

        if self.room_name == "stranger":
            send_stranger_static()

        if self.room_name == "fall":
            send_fall_static()

        if self.room_name == "attack":
            send_attack_static()

        print("来了新连接")
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print(self.room_group_name)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))