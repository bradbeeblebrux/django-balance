from django.contrib import admin

# Register your models here.

from .models import Owner, Account, Category, Excluded_Category,Excluded_Action, Transaction

admin.site.register(Owner)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Excluded_Category)
admin.site.register(Excluded_Action)
admin.site.register(Transaction)

