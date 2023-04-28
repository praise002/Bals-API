from django.urls import path
from . views import SubscriberCreateAPIView, SubscriberDestroyAPIView

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', SubscriberCreateAPIView.as_view(), name='create_subscriber'),
    path('unsubscribe/', SubscriberDestroyAPIView.as_view(), name='delete_subscriber'),
]
