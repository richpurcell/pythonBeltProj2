from django.conf.urls import url
from . import views
        
urlpatterns = [
        url(r'^$', views.show_dashboard),
        url(r'^new$', views.new_wish),
        url(r'^add$', views.add_wish),
        url(r'^stats$', views.wish_stats),
        url(r'like/(?P<wish_id>\d+)$', views.like_wish),
        url(r'^edit/(?P<wish_id>\d+)$', views.wish_edit),
        url(r'^edit/wish/(?P<wish_id>\d+)$', views.edit_wish),
        url(r'^remove/(?P<wish_id>\d+)$', views.remove_wish),
        url(r'^granted/(?P<wish_id>\d+)$', views.grant_wish),
        url(r'^logout$', views.log_out),
]
