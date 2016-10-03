from django.contrib import admin

# Register your models here.

from .models import Owner, Account, Category, Transaction

admin.site.register(Owner)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Transaction)

