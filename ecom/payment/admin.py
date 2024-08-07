from django.contrib import admin
from .models import ShippingAddress,Order,OrderItems


# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(OrderItems)
admin.site.register(Order)