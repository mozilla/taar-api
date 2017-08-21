from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^recommendations/(?P<client_id>[0-9a-f]{32})/$',
        views.recommendations, name='recommendations'),
]
