from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^flavors$',views.flavors),
    url(r'^gallery$',views.gallery),
    url(r'^reservations$',views.book),
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
    url(r'^logout$',views.logout),
    url(r'^admin$',views.adminHome),
    url(r'^admin/addCarouselItem$',views.addCarouselItem),
    url(r'^admin/saveCarouselEdits$',views.saveCarouselEdits),
    url(r'^admin/deleteCarouselItem/(?P<id>\d+)$',views.deleteCarouselItem),
    url(r'^adminFlavors$',views.adminFlavors),
    url(r'^admin/addFlavorItem$',views.addFlavorItem),
    url(r'^admin/saveFlavorEdits$',views.saveFlavorEdits),
    url(r'^admin/deleteFlavorItem/(?P<id>\d+)$',views.deleteFlavorItem),
    url(r'^adminGallery$',views.adminGallery),
    url(r'^admin/addGalleryItem$',views.addGalleryItem),
    url(r'^admin/deleteGalleryItem/(?P<id>\d+)$',views.deleteGalleryItem),
    url(r'^admin/reservations$',views.adminHome),
    url(r'^admin/contactus$',views.adminContactUs),
    url(r'^admin/reviews$',views.adminHome),
    url(r'^admin/manage/orders$',views.adminHome),
    url(r'^admin/manage/users$',views.adminHome)
]