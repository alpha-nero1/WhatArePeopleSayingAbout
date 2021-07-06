from django.contrib import sitemaps
from app.models import Topic
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = 'https'

    def get_urls(self, site=None, **kwargs):
        site = sitemaps(domain='whatarepeoplesayingabout.com', name='whatarepeoplesayingabout.com')
        return super(StaticSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return ['/', '/login', '/signup']

    def location(self, item):
        return item


class TopicSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def get_urls(self, site=None, **kwargs):
        site = sitemaps(domain='whatarepeoplesayingabout.com', name='whatarepeoplesayingabout.com')
        return super(StaticSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return Topic.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at
        
    def location(self,obj):
        return '/topics/%s' % (obj.kebab_name)
    