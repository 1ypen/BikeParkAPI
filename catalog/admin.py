from django.contrib import admin

from .models import Bicycle, Brand, Media, Price, Order, OrderDetail

admin.site.register(Bicycle)
admin.site.register(Brand)
admin.site.register(Media)
admin.site.register(Price)
admin.site.register(Order)
admin.site.register(OrderDetail)