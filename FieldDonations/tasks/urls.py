from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.OfficeView.as_view(), name='index'),
    url(r'^nearby/(?P<lat>.*)/(?P<lon>.*)/(?P<limit>\w+)$', views.NearbyOfficeView.as_view(), name='nearby'),
    url(r'^office/(?P<pk>[-\w]+)$', views.SingleOfficeView.as_view(), name='single_office'),
    url(r'^items$', views.ItemView.as_view(), name='items'),
    url(r'^search-field-offices/$', views.SearchFieldOfficeView, name='search-field-offices'),
]
