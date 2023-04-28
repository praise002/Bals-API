from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9  # the max is 1
    
    def items(self):
        # return Post.objects.filter(status='PB')
        return Post.published.all()
    
    def lastmod(self, obj):  # the last time the obj was modified
        return obj.updated
    
    def location(self, obj):
        return reverse('blog:post_detail', args=[obj.pk, obj.slug])
