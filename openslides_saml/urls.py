from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^saml/$', views.IndexView.as_view()),
    url(r'^saml/metadata/$', views.serve_metadata),
]
