from django.contrib import admin
from . models import Invoice, Client, Vendor, ProjectItem


admin.site.register(Invoice)
admin.site.register(Client)
admin.site.register(Vendor)
admin.site.register(ProjectItem)
