from django.db import models
from django.utils import timezone
import secrets

class TimeBaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at =models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Newsletter(TimeBaseModel):
    # title, body, created_at, updated_at
    title = models.CharField(max_length=250)
    body = models.TextField()
    
    
class Subscriber(TimeBaseModel):
    # email, confirmed, confirmation_token
    email = models.EmailField(max_length=50, unique=True)
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=250, blank=True)
    
    def generate_confirmation_token(self):
        self.confirmation_token = secrets.token_urlsafe()
        self.save()
