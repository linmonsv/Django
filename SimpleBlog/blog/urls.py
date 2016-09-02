from django.conf.urls import *
from blog.views import archive
urlpatterns = [
    url(r'^$', archive)
]
