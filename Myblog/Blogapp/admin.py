from django.contrib import admin
from Blogapp.models import User_Reg,Post,Comment

@admin.register(User_Reg)
class UserRegAdmin(admin.ModelAdmin):
    list_display = ("usertype","user__first_name","user")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display =("title","short_description","description","created_by","user")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display =("user","content","created_at")