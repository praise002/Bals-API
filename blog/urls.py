from django.urls import path, include
from . views import PostList, PostDetail, CommentList, \
CommentDetail, PostRecommendationsView, PostSearchListAPIView, LatestPostsView

app_name = 'blog'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('search/', PostSearchListAPIView.as_view(), name='post_search'),
    path('comments/', CommentList.as_view(), name='comment_list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment_detail'),
    path('latest-posts/', LatestPostsView.as_view(), name='latest_posts'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),  
    path('<slug:slug>/recommendations/', PostRecommendationsView.as_view(), name='post_recommendations'),
]


