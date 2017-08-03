from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^recommendations/(?P<uuid>[0-9a-f]{32})/$',
        views.recommendations, name='recommendations'),
]
