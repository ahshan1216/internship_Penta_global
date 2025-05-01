# accounts/admin.py
from django.contrib import admin
from .models import User, AccountHolder, Moderator, Transaction

admin.site.register(User)
admin.site.register(AccountHolder)
admin.site.register(Moderator)
admin.site.register(Transaction)
