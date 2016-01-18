# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Account, Owner, Transaction, Category, \
    Transaction_to_Category, Word_to_Category, \
    Excluded_Category, Excluded_Action
from django.utils.translation import ugettext as _


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'reference', 'description', 'amount', 'get_owner', 'get_account', 'comment')
    list_filter = ['date']
    search_fields = ['description', 'reference']

    def get_account(self, obj):
        return obj.account.name
    get_account.short_description = u'חשבון'

    def get_owner(self, obj):
        return obj.owner.name
    get_owner.short_description = u'בעלים'

admin.site.register(Account)
admin.site.register(Owner)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
admin.site.register(Transaction_to_Category)
admin.site.register(Word_to_Category)
admin.site.register(Excluded_Category)
admin.site.register(Excluded_Action)
