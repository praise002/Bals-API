from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.DRAFT)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class Post(BaseModel):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    body = models.TextField()
    slug = models.SlugField(max_length=250)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    # tag
    
    objects = models.Manager()  #the default manager
    published = PublishedManager()  #our custom manager
    
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    
    
class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') #associate each comment with a single post
    name = models.CharField(max_length=10)
    email = models.EmailField()
    body = models.TextField()
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
