from django.urls import path
from .views import (
    UserRegistration, 
    UserLogin,
    CreatePost,
    DeletePost,
    UpdatePost,
    AllViewForPost,
    CreatComment,
    CommentDetails,
    DeleteComment,
)


urlpatterns = [
    #                         For Authentications
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),


    #                         For Posts
    path('createpost/', CreatePost.as_view(), name='createpost'),
    path('createpost/<int:pk>/', CreatePost.as_view(), name='createpost'), #for get
    path('deletepost/<int:pk>/', DeletePost.as_view(), name='deletepost'),
    path('updatepost/<int:pk>/', UpdatePost.as_view(),name="updatepost"),
    path('allpost/', AllViewForPost.as_view(), name="allpost"),
    #path('userbasepostview/', UserView.as_view(), name='userbasepostview'), 


    #                         For Comments
    #path('comment/<int:pk>/', CreatComment.as_view(), name='comment'),
    path('commentdetails/<int:pk>/', CommentDetails.as_view(), name='commentdetails'),
    path('commentdetails/',CommentDetails.as_view(), name='commentdetails'),
    path('deletecomment/<int:pk>/', DeleteComment.as_view(), name='deletecomment')  #delete and get the comment
]