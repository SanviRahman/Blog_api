from django.urls import path
from .views import (
    UserRegistrationView, 
    UserLoginView,
    BlogCreateView,
    BlogDeleteView,
    BlogUpdateView,
    BlogAllView,
    BlogUserView,
)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('create/<int:pk>/', BlogCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', BlogUpdateView.as_view(),name="update"),
    path('all/', BlogAllView.as_view(), name="all"),
    path('userbase/', BlogUserView.as_view(), name='userbase')
]