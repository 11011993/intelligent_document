from django.db import models
from django.contrib.auth.models import User

class UploadDocument(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='pdfs/',null=True,blank=True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)

