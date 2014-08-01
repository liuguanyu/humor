from django.db import models

from django.db import models

class Joke(models.Model):
    title = models.CharField(max_length=255)
    user_id = models.IntegerField()
    url = models.CharField(max_length=4096)
    msg = models.TextField()
    create_time = models.DateTimeField()