from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/', views.register, name="register"),
    url(r'^registration_ok/$', views.registration_ok, name="registration_ok"),
    url(r'^logged_out/$', views.logged_out, name="logged_out"),
]
