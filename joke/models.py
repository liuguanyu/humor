from django.db import models

class Joke(models.Model):
    title = models.CharField(max_length=255)
    user_id = models.IntegerField()
    url = models.CharField(max_length=4096,blank=True)
    msg = models.TextField(default="")
    create_time = models.DateTimeField(auto_now_add=True)