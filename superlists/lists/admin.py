from django.contrib import admin
from lists.models import Item

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)
