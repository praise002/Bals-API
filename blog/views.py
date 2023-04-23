from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostList(generics.ListCreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.published.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    
class CommentList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class CommentDetail(generics.RetrieveDestroyAPIView):
    # anonymous users can comment on a post
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    # TODO: build it to be seo-friendly, slug and uuid, using canonical url in APIView
    
