from django.contrib import admin
from .models import User,store,product,order,chat

admin.site.register(User)
admin.site.register(store)
admin.site.register(product)
admin.site.register(order)
admin.site.register(chat)
# Register your models here.
