from django.conf.urls import patterns, url

from .views import FindComparableView


urlpatterns = patterns('',
    url(r'^find', FindComparableView.as_view(),
        name='sizecompare_find_comparable'),
)
