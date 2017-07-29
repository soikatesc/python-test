from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^products$',views.products),
	url(r'^products/(?P<purchase_id>\d+)/purchase_complete',views.purchase_complete),
	url(r'^products/(?P<product_id>\d+)/purchase',views.product_purchase),
	url(r'^products/(?P<product_id>\d+)/details',views.product_details),
]

	