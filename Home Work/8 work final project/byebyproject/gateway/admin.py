from django.contrib import admin
from .models import Role, AssignRole, Marchant, Client, Transaction,Agent

# Register your models here.
admin.site.register(Role)
admin.site.register(AssignRole)
admin.site.register(Marchant)
admin.site.register(Client)
admin.site.register(Transaction)
admin.site.register(Agent)