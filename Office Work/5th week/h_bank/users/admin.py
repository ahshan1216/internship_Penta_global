from django.contrib import admin
from .models import Role,UserRole,ModeratorProfile,AccountHolderProfile,Transaction

# Register your models here.
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(ModeratorProfile)
admin.site.register(AccountHolderProfile)
admin.site.register(Transaction)