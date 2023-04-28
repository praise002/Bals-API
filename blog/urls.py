from django.urls import path, include
from . views import PostList, PostDetail, CommentList, CommentDetail, PostRecommendationsView, PostSearchListAPIView

app_name = 'blog'

urlpatterns = [
    path('', PostSearchListAPIView.as_view(), name='post_search'),
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/<slug:slug>/', PostDetail.as_view(), name='post_detail'),  
    path('posts/<int:post_id>/<slug:slug>/recommendations/', PostRecommendationsView.as_view(), name='post_recommendations'),
    path('comments/', CommentList.as_view(), name='comment_list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
]

