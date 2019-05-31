from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Cliente, Dependente

class ClienteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cliente, ClienteAdmin)

class DependenteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Dependente, DependenteAdmin)