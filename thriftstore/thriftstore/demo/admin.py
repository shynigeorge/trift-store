from django.contrib import admin
from .models import *
#
# Register your models here.
admin.site.register(customer)
admin.site.register(CustomerDetails)
admin.site.register(staff)
admin.site.register(Seller_Product)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Cart)
admin.site.register(Items)
admin.site.register(Card)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(Courier_Assign)

