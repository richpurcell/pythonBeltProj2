from django.conf.urls import url
from . import views
        
urlpatterns = [
        url(r'^$', views.show_login),
        url(r'^process/login$', views.process_login),
        url(r'^process/registration$', views.process_registration),
        url(r'^success$', views.show_success),
        # url(r'^wishes$', views.show_dashboard),
        url(r'^logout$', views.log_out),
]
