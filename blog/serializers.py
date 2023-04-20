from rest_framework import serializers
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from .models import Post, Comment


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        fields = ['id', 'author', 'title', 'body', 'slug', 'publish', 'tags', 'comments']
        model = Post
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'email', 'body']
        model = Comment