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
    path('pending-posts/',PendingPostView.as_view(),name='pending_posts'),                              #new path
    path('approve-post/<int:post_id>/',ApprovePostView.as_view(),name='approve_post'),                  #new path
    path('reject-post/<int:post_id>/',RejectPostView.as_view(),name='reject_post'),                     #new path
    path('search/', SearchPostView.as_view(), name='search_posts'),                                     #new path
    path('profile/', ProfileView.as_view(), name='profile'),                                            #new path
    path('myposts/', MyPostsView.as_view(), name='myposts'),
    path('viewpost/',ViewPost.as_view(),name="viewpost"),
    path('descpost/<int:id>/',DetailedPost.as_view(),name="detailpost"),
    path('updatepost/<int:id>/',UpdatePost.as_view(),name="updatepost"),
    path('deletepost/<int:id>/',DeletePost.as_view(),name='deletepost'),
    path('recentpost/',RecentpostView.as_view(),name="recentpost"),
    path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),
    path('dislike/<int:post_id>/', DislikePostView.as_view(), name='dislike_post'),
    path('pythonstart/',PythonStartView.as_view(), name="pythonstart"),
    path('webdesign/', WebDesigntipsView.as_view(), name="webdesigntips"),
    path('djangoadvantage/',DjangoadvantageView.as_view(), name="djangoadvantage")
]
