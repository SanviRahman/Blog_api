
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from .models import Blog
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404




# create a views for userRegsitrations
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#Create a Login Views
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)


        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
               {
                     'message': 'You have successfully logged in',
                     'token': {
                            "refresh":str(refresh),
                            "access":str(refresh.access_token)},
               },
                status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



#write a new view for create views
class BlogCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the logged-in user as the author
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def get(self, request,pk):
        blog = get_object_or_404(Blog, pk=pk)
        if blog.author == request.user:
            serializer = BlogSerializer(blog)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'You are not authorized to view this blog.'},
                status=status.HTTP_403_FORBIDDEN,
            )

    


#write a new view for delete views

class BlogDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        if blog.author == request.user:
            blog.delete()
            return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'Blog not deleted'}, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request,pk):
        blog = get_object_or_404(Blog, pk=pk)
        if blog.author == request.user:
            serializer = BlogSerializer(blog)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'You are not authorized to view this blog.'},
                status=status.HTTP_403_FORBIDDEN,
            )
    

class BlogUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        # Retrieve the blog post or return a 404 error if not found
        blog = get_object_or_404(Blog, pk=pk)
        # Check if the requesting user is the author of the blog post
        if blog.author != request.user:
            return Response(
                {"error": "You do not have permission to edit this blog."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Deserialize and validate the incoming data
        serializer = BlogSerializer(blog, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()  # Save the changes
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

     
    def get(self, request,pk):
        blog= get_object_or_404(Blog, pk=pk)
        if blog.author == request.user:
            serializer = BlogSerializer(blog)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'You are not authorized to view this blog.'},
                status=status.HTTP_403_FORBIDDEN,
            )
    

#write a new views for show all data read

class BlogAllView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    

#write a views logged in user base can see only his  views
class BlogUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        blogs = Blog.objects.filter(author=request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    


#create a new views for logged in user can comment on his blog
class BlogCommentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        if blog.author == request.user:
            serializer = BlogSerializer(blog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'message': 'You are not authorized to comment on this blog.'},
                status=status.HTTP_403_FORBIDDEN,
                )
        


#show all comments with user details
class BlogCommentAllView(APIView):
    def get(self, request):
        comments = Blog.objects.filter(comments__isnull=False).values('author__id', 'author__username','comments')
        return Response(comments)
    


#write a class to delete comments
class BlogDeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # Fetch the specific blog by its primary key
        blog = get_object_or_404(Blog, pk=pk)

        # Check if the current user is the author of the blog
        if blog.author == request.user:
            # Clear the comments field
            blog.comments = None
            blog.save()

            return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)