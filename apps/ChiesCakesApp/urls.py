from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^flavors$',views.flavors),
    url(r'^gallery$',views.gallery),
    url(r'^book$',views.book),
    url(r'^contacts$',views.contacts),
    url(r'^reviews$',views.reviews),
    url(r'^register$',views.register),
    url(r'^reserve/(?P<day>\d+)/(?P<month>\d+)$',views.reserve),
    url(r'^newuser$',views.newuser),
    url(r'^login$',views.login,),
    url(r'^process$',views.process),
    url(r'^editProcess/(?P<day>\d+)/(?P<month>\d+)$',views.editProcess),
    url(r'^post_review$',views.post_review),
    url(r'^post_comment$',views.post_comment), 
    url(r'^logout$',views.logout)
]