from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<product_id>[0-9]+)/$', views.results, name="results"),
    url(r'^search/$', views.search, name="search"),
    url(r'^product_detail/(?P<product_id>[0-9]+)/$',
        views.product_detail,
        name="product_detail"),
    url(r'^user_products/$', views.user_products, name="user_products"),
    url((r'^save_product/(?P<product_selected_id>[0-9]+)'
         r'/(?P<substitution_id>[0-9]+)/$'),
        views.save_product, name="save_product"),
    url(r'^delete_product/(?P<product_id>[0-9]+)/$',
        views.delete_product,
        name="delete_product"),
    url(r'^legal/$', views.legal, name="legal")
]
