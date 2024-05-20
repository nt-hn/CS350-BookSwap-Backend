from django.db import models
from account_api.models import User
# Create your models here.
class CreateChat(models.Model):
    chat_member_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_member_1')
    chat_member_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_member_2')

    def __str__(self):
        return str(self.id)
    
class Chat(models.Model):
    chatroom = models.ForeignKey(CreateChat, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.text
