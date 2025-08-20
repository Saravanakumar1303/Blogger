from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class User_Reg(models.Model):
    User_types =[
        ('admin','Admin'),
        ('creator','Creator'),
        ('reader','Reader'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    usertype=models.CharField(max_length=55,choices=User_types)

class Post(models.Model):
    title = models.CharField(max_length=55)
    short_description = models.TextField(max_length=400)
    description = models.TextField(max_length=1000)
    created_by =models.DateField(auto_now_add=True)
    user =models.ForeignKey(User,on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)