from django.contrib import admin
from .models import CollectionAgency, CollectionFiles, Client, Consumer, Debt

# Register your models here.
admin.site.register(CollectionAgency)
admin.site.register(CollectionFiles)
admin.site.register(Client)
admin.site.register(Consumer)
admin.site.register(Debt)
