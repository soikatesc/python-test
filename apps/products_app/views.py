from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Count

def index(request):
	context = {
		"selected": "home"
	}
	return render(request, "products_app/index.html", context)

def products(request):
	products = Product.objects.all()
	context = {
		'products' : products,
		'selected' : "products"
	}
	return render(request, "products_app/products.html", context)

def product_details(request, product_id):
	product = Product.objects.filter(id=product_id).first()
	if not product:
		return redirect('/products')
	context = {
		"product": product,
	}
	return render(request, "products_app/product_detail.html", context)

def product_purchase(request, product_id):
	product = Product.objects.filter(id=product_id).first()
	if request.method != 'POST':
		if not product:
			return redirect('/products')
		if product.inventory < 1:
			return redirect('/products')
		context = {
			"product": product,
		}
		return render(request, "products_app/product_purchase.html", context)
	else:
		check = Purchase.objects.validatePurchase(request.POST)
		if check[0] == False:
			for error in check[1]:
				messages.error(request,error)
			return redirect('/products/{}/purchase'.format(product_id))
		else:
			purchase_id = Purchase.objects.order_creation(request.POST, product_id)
			if purchase_id == False:
				messages.error(request,"Not enough inventory")
				return redirect('/products/{}/purchase'.format(product_id))
			else:
				return redirect('/products/{}/purchase_complete'.format(purchase_id))

def purchase_complete(request, purchase_id):
	purchase = Purchase.objects.filter(id=purchase_id).first()
	
	if not purchase:
		return redirect('/products')
	context = {
		"purchase" : purchase
	}
	return render(request, "products_app/purchase_complete.html", context)



