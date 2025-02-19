from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    date=models.DateTimeField()
    flexibility=models.IntegerField()
    departure_place=models.TextField()
    destination_place=models.TextField()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    # task = models.ForeignKey(task, on_delete=models.CASCADE,null=False,blank=False,default=1)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if not self.task_id:  # If no task is set
    #         first_task = task.objects.first()  # Get the first Task in DB
    #         if first_task:
    #             self.task = first_task
    #     super().save(*args, **kwargs)
