from django.contrib.sitemaps import Sitemap
from movies.models import Movie


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Movie.objects.all()