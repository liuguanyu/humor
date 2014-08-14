from django.db import models

# Create your models here.
class Images(models.Model):
    url = models.CharField(max_length=4096)
    md5 = models.CharField(max_length=32, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

class ImageDelegate :
    @staticmethod
    def insertImgs (imgs) :
        for img in imgs :
            try:
                imgModel = Images(url=img["url"] , md5=img["hsh"])
                imgModel.save()
            except :
                pass