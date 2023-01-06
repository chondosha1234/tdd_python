from django.contrib import admin
from lists.models import Item, List

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    pass


class ListAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)
admin.site.register(List, ListAdmin)
