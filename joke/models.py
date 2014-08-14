from django.db import models

class Joke(models.Model):
    title = models.CharField(max_length=255)
    user_id = models.IntegerField()
    url = models.CharField(max_length=4096,blank=True)
    msg = models.TextField(default="")
    msg_md5 = models.CharField(max_length=40, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

class JokeDelegate :  
    @staticmethod
    def insertJokes (jokes) :
        for joke in jokes :
            print joke
            try:
                jokeModel = Joke(
                    title = joke["title"] , 
                    user_id = joke["user_id"] ,
                    url = joke["url"] , 
                    msg_md5 = joke["content_md5"] ,
                    msg = joke["content"]
                )
                jokeModel.save()
            except Exception , e:
                print e
                pass

class User(models.Model):  
    user_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)        