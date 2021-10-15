from django.contrib import admin

from .models import *


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SelectedProduct)
admin.site.register(Selection)
admin.site.register(UserClass)
admin.site.register(Order)


