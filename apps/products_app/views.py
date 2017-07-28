from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Count

def index(request):	
	return render(request, "products_app/index.html")

def products(request):
	products = Product.objects.all()
	context = {
		'products' : products
	}
	return render(request, "products_app/products.html", context)

def product_details(request, product_id):
	product = Product.objects.filter(id=product_id).first()
	context = {
		"product": product,
	}
	return render(request, "products_app/product_detail.html", context)

def product_purchase(request, product_id):
	product = Product.objects.filter(id=product_id).first()
	context = {
		"product": product,
	}
	return render(request, "products_app/product_purchase.html", context)

def create_order(request, product_id):
	if request.method != 'POST':
		return redirect('/')
	else:
		check = Purchase.objects.validatePurchase(request.POST)
		# print check
		if check[0] == False:
			for error in check[1]:
				print error
				messages.error(request,error)
			return redirect('/products/{}/purchase'.format(product_id))
		else:
			purchase_id = Purchase.objects.order_creation(request.POST, product_id)
			return redirect('/products/{}/purchase_complete'.format(purchase_id))

def purchase_complete(request, purchase_id):
	purchase = Purchase.objects.filter(id=purchase_id).first
	context = {
		"purchase" : purchase
	}
	return render(request, "products_app/purchase_complete.html", context)



