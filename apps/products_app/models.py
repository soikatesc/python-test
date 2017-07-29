from __future__ import unicode_literals

from django.db import models
import re
import uuid

# Create your models here.
class PurchaseManager(models.Manager):
	def validatePurchase(self, post):
		is_valid = True
		errors = []

		if len(post.get('byer_name'))<2 and not re.search(r'\w+',post.get('byer_name')):
			is_valid = False
			errors.append('Name is required, and cannot be number')

		if not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',post.get('byer_email')):
			is_valid = False
			errors.append('Enter a valid email, eg: example@example.com')

		if not re.search(r'\d{3}\d{3}\d{4}', post.get('byer_phone')):
			is_valid = False
			errors.append('Enter a valid mobile number, eg: 1234567890')

		return (is_valid, errors)

	def my_random_string(self, string_length=10):
	    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
	    random = random.upper() # Make all characters uppercase.
	    random = random.replace("-","") # Remove the UUID '-'.
	    return random[0:string_length] # Return the random string.

	def order_creation(self, post, product_id):

		p = Product.objects.get(id=product_id)
		if p.inventory <= 0:
			return False
		else:
			p.inventory = p.inventory - 1
			p.save()

			purchase = Purchase.objects.create(
				byer_name = post.get('byer_name'),
				byer_email = post.get('byer_email'),
				byer_phone = post.get('byer_phone'),
				product = p,
				confirmation_code = self.my_random_string(6)
			)
			return purchase.id
	# generating random string


class Product(models.Model):
	name = models.CharField(max_length=255)
	price = models.IntegerField()
	inventory = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "Name: {}, Price: {}, Inventory: {} ".format(self.name, self.price, self.inventory)


class Purchase(models.Model):
	confirmation_code = models.CharField(max_length=255)
	byer_name = models.CharField(max_length=255)
	byer_email = models.CharField(max_length=255)
	byer_phone = models.CharField(max_length=255)
	product = models.ForeignKey(Product,related_name="purchases")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = PurchaseManager()

	def __str__(self):
		return "Confirmation Code: {}, Byer Name: {}, Byer Email: {}, Byer Phone: {}".format(self.confirmation_code, self.byer_name, self.byer_email, self.byer_phone)