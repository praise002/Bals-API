from django.urls import path
from . views import PostList, PostDetail, CommentList, CommentDetail
app_name = 'blog'

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/<slug:slug>/', PostDetail.as_view(), name='post_detail'),  
    path('comments/', CommentList.as_view(), name='comment_list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
]

