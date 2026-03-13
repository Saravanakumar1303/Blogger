from django.shortcuts import render,redirect,get_object_or_404
import re
from django.contrib import messages
from Blogapp.models import User_Reg
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model,authenticate,login,logout
from Blogapp.models import Post,Comment,Like
from django.core.paginator import Paginator

# Create your views here.

class HomeView(View):
    """
    This is homepage
    """
    def get(self,request):
        return render(request,'home.html')

class RecentPostView(View): 
    def get(self, request):
        return render(request, 'recent.html')
    
class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    
    def post(self,request):
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        usertype=request.POST.get('usertype')

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        password_pattern = r'^(?=.*[A-Z])(?=.*\d).{6,}$'

        if not re.match(email_pattern,email):
            messages.error(request,'Invalid Email Format.')
            return redirect('register')
        
        if not re.match(password_pattern,password):
            messages.error(request,'Password must contain at least 6 characters, one uppercase letter, and one digit.')
            return redirect('register')
        
        if get_user_model().objects.filter(email=email):
            messages.error(request,'Email already registered.')
            return redirect('register')

        user_obj = get_user_model().objects.create(
            first_name = fname,
            last_name = lname,
            email = email,
            password = password,
            username =email
        )
        user_obj.set_password(password)
        user_obj.save()

        User_Reg.objects.create(
            user = user_obj,
            usertype = usertype
        )
        messages.success(request,'Registration Successful! Please login.')
        return redirect('login')
        
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        username =request.POST.get('username')
        password = request.POST.get('password')
        #print("Email :",username)
        #print("Password :",password)

        if username and password:
            user = authenticate(request,username=username,password=password)
            #print("User :",user)
            if user:
                login(request,user)
                messages.error(request,"Login Succesfully!")
                return redirect('home')
            else:
                messages.error(request,'Invalid Email or password!')
                return redirect("login")
        print("Invalid Email or password!")
        messages.error(request,"Invalid Email or password")
        return redirect("login")
        
class Logoutview(View):
    def get(self,request):
        logout(request)
        return redirect('home')
    
class CreatePost(LoginRequiredMixin,View):
    def get(self,request):
        user_role = User_Reg.objects.filter(user=request.user).first()
        if not user_role:
            messages.error(request,"User role not found")
            return redirect('detailpost')

        if user_role.usertype == "reader":
            messages.error(request,"Reader cannot create post")
            return redirect('detailpost')
        return render(request,'postcreate.html')

    def post(self,request):
        title = request.POST.get('title')
        short_description = request.POST.get('short_des')
        description = request.POST.get('des')

        if title and description:
            Post.objects.create(
                user = request.user,
                title = title,
                short_description = short_description,
                description = description
            )
            return redirect('viewpost')
        
class ViewPost(View):
    def get(self,request):
        post_obj =Post.objects.all().values('id','title','description','short_description','user__first_name','created_by').order_by('-created_by')
        paginators = Paginator(post_obj, 5)
        page_numbers = request.GET.get('page')
        page_obj = paginators.get_page(page_numbers)
        return render(request,'viewpost.html',{'post':page_obj})


class DetailedPost(View):
    def get(self,request,id):
        type = None
        user_obj =User_Reg.objects.filter(user=request.user)
        if user_obj:
            user_obj = user_obj.first()
            type =user_obj.usertype #type:ignore
        print("type",type)
        post_obj = Post.objects.filter(id=id).values('id','title','description','user__first_name','created_by')[0]
        comments = Comment.objects.filter(post_id=post_obj.get("id")).order_by("-created_at")
        return render(request,'full_des.html',{'detpost':post_obj,'type':type,'cmd':comments})
    
    def post(self, request, id):
        post = Post.objects.get(id=id)
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
        return redirect("detailpost", id=id)
    

class UpdatePost(View):
    def get(self,request,id):
        try:
            post = Post.objects.filter(id=id).first()
            if post:

                if post.user != request.user:
                    messages.error(request,"You cannot edit this post")
                    return redirect('detailpost')
                return render(request,'updatepost.html',{'post':post})
        except Exception as e:
            print("Exception :",e)
        return redirect('detailpost')
    
    def post(self,request,id):
        try:
            post = Post.objects.filter(id=id).first()
            #print("post",post)
            if post:
                if post.user != request.user:
                    messages.error(request,"Permission denied")
                    return redirect('detailpost')
                post.title = request.POST.get('title',post.title) # type: ignore
                post.short_description = request.POST.get('short_description',post.short_description) # type: ignore
                post.description = request.POST.get('description',post.description) # type: ignore
                post.save() # type: ignore
                return redirect(f'/descpost/{post.id}') # type: ignore
        except Exception as e:
            print("Expection :",e)
        return redirect(f'/updatepost/{post.id}/') #type: ignore

class DeletePost(View):
    def get(self,request,id):
        post = Post.objects.get(id=id)
        post.delete() # type: ignore
        return redirect("viewpost")

class RecentpostView(View):
    def get(self,request):
        post= Post.objects.all().values('id','title','short_description','user__first_name','created_by').order_by('-created_by')[:5]
        return render(request,'recentpost.html',{'post':post})

class LikePostView(LoginRequiredMixin,View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        try:
            reaction = Like.objects.get(user=user, post=post)

            if reaction.value == 1:
                reaction.delete()
            else:
                reaction.value = 1
                reaction.save()
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post, value=1)
        return redirect(request.META.get('HTTP_REFERER'))
    
class DislikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        try:
            reaction = Like.objects.get(user=user, post=post)
            if reaction.value == -1:
                reaction.delete()
            else:
                reaction.value = -1
                reaction.save()
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post, value = -1)
        return redirect(request.META.get('HTTP_REFERER'))