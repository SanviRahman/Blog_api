
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, BlogSerializer, CommentSerializer
from django.contrib.auth.models import User
from .models import Blog, Comment
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404




# create a views for userRegsitrations
class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#Create a Login Views
class UserLogin(APIView):
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







 #              CRUD Operations
#write a new view for create views
class CreatePost(APIView):
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

    


#update views
class UpdatePost(APIView):
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
    

#write a new view for delete views
class DeletePost(APIView):
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
        






#                AllView For Post
#write a new views for show all data read
class AllViewForPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = Blog.objects.all() 

        blog_data = []

        for blog in blogs:
            # Fetch the author details of this blog
            blog_serializer = BlogSerializer(blog)

            # Fetch the comments related to this blog
            comments = blog.comment.all()  # related_name='comment' 
            comment_serializer = CommentSerializer(comments, many=True)

            
            blog_data.append({
                "post_details": {
                    "Blog_id": blog.id,
                    "image": blog.image.url if blog.image else None,
                    "title": blog.title,
                    "description": blog.description,
                    "author": blog.author.username,
                    "comments": comment_serializer.data,  
                    "created_at": blog.created_at,
                    "updated_at": blog.updated_at
                }
            })

        return Response(blog_data, status=status.HTTP_200_OK)








 #                  comments
#write comments view where has comments
class CreatComment(APIView):
    permission_classes = [IsAuthenticated]
    
    # To create a new comment on the blog
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        
        # Ensure the request contains a 'comment' field in the data
        comment_data = request.data.get('comment')
        if not comment_data:
            return Response({'message': 'Comment is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new comment for the blog
        comment = Comment.objects.create(
            blog=blog,
            user=request.user,
            comment=comment_data
        )
        
        # Serialize the comment object to return it in the response
        comment_serializer = CommentSerializer(comment)
        return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
    





#show all comments with user details and post
class CommentDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        blogs = Blog.objects.all()
        
        blog_data = []
        
        for blog in blogs:
            # Serialize blog details (only title and description)
            blog_serializer = BlogSerializer(blog)
            
            # Serialize the author's username
            author_username = blog.author.username if blog.author else "Unknown"

            # Serialize the comments
            comments = blog.comment.all()
            comment_serializer = CommentSerializer(comments, many=True)

            # Append filtered data to the response list
            blog_data.append({
                "title": blog_serializer.data["title"],
                "description": blog_serializer.data["description"],
                "username": author_username,
                "comments": comment_serializer.data
            })

        return Response(blog_data, status=status.HTTP_200_OK)
    
    #create a views for single blog
    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        serializer = BlogSerializer(blog)
        author_username = blog.author.username if blog.author else "Unknown"
        comments = blog.comment.all()
        comment_serializer = CommentSerializer(comments, many=True)
        return Response({
            "title": serializer.data["title"],
            "description": serializer.data["description"],
            "username": author_username,
            "comments": comment_serializer.data
        }, status=status.HTTP_200_OK)
    






# write a class to delete comments
class DeleteComment(APIView):
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