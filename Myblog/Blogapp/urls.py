from django.contrib import admin
from django.urls import path
from Blogapp.views import *

urlpatterns =[
    path('admin/',admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('createpost/',CreatePost.as_view(),name="createpost"),
    path('viewpost/',ViewPost.as_view(),name="viewpost"),
    path('descpost/<int:id>/',DetailedPost.as_view(),name="detailpost"),
    path('updatepost/<int:id>/',UpdatePost.as_view(),name="updatepost"),
    path('deletepost/<int:id>/',DeletePost.as_view(),name='deletepost'),
    path('recentpost/',RecentpostView.as_view(),name="recentpost"),
]
