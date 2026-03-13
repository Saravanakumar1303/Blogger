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

class Like(models.Model):
    Like_Choices =(
        (1, 'Like'),
        (-1, 'Dislike')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=Like_Choices)

    class Meta: 
        unique_together = ('user', 'post')