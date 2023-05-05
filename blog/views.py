from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q, Value, CharField
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
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
    
class PostSearchListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination = None
    
    def get_queryset(self):
        queryset = Post.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.annotate(
                search=Concat('title', Value(' '), 'body', output_field=CharField())  # combine into a single field
            ).filter(
                Q(title__icontains=search_query) | Q(body__icontains=search_query) |
                Q(search__icontains=search_query) | Q(tags__name__icontains=search_query)
            ).distinct()  # check if these fields contains the search query
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)
    
class LatestPostsView(APIView):
    def get(self, request):
        latest_posts = Post.published.order_by('-publish')[:10]
        serializer = PostSerializer(latest_posts, many=True)  # serializing multiple objs at once
        return Response(serializer.data)
    
class CommentList(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class CommentDetail(generics.RetrieveDestroyAPIView):
    # anonymous users can comment on a post
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class PostRecommendationsView(generics.ListAPIView):
    serializer_class = PostSerializer
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug=slug)
        
        # get all tags for current post
        tags = post.tags.all()
        
        # get all posts that are tagged with any of those tags
        posts = Post.objects.filter(tags__in=tags).distinct()
        
        # exclude current post from the list of recommended posts
        posts = posts.exclude(slug=slug)
        
        # order by number of tags shared with current post, then by recency
        posts = posts.annotate(shared_tags=Count('tags', filter=Q(tags__in=tags))).order_by('-shared_tags', '-created')
        
        # limit the number of recommended posts
        limit = self.request.query_params.get('limit', 10)
        return posts[:int(limit)]

