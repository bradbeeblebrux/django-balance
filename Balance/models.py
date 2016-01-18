# -*- coding: utf-8 -*-
from django.db import models


class Owner(models.Model):
    name = models.CharField('שם', max_length=20)

    def __unicode__(self):
        return self.name


class Account(models.Model):
    name = models.CharField('שם', max_length=100)
    _class = models.CharField('שייכות', max_length=100)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField('תאריך פעולה')
    reference = models.CharField('אסמכתא', max_length=40)
    description = models.CharField('תאור', max_length=100)
#    full_amount = models.DecimalField('סכום מלא', decimal_places=2, max_digits=8)
#    current_amount = models.DecimalField('סכום לתשלום', decimal_places=2, max_digits=8)
    amount = models.DecimalField('סכום', decimal_places=2, max_digits=8)
    owner = models.ForeignKey(Owner)
    account = models.ForeignKey(Account)
    comment = models.TextField('הערות', blank=True)

    def __unicode__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.date, self.reference, self.description, self.owner.name, self.account.name, self.comment)

    @classmethod
    def get_years(cls):
        return list(set([trans.date.year for trans in cls.objects.all()]))


class Category(models.Model):
    name = models.CharField('תיאור', max_length=20)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_categories(cls):
        return list(set([cat.name for cat in cls.objects.all()]))


class Transaction_to_Category(models.Model):
    category = models.ForeignKey(Category, verbose_name='ו')
    transaction = models.ForeignKey(Transaction)
    comment = models.TextField('הערות', blank=True)

    def __unicode__(self):
        return "%s - %s - %s" % (self.category.name, self.transaction.reference, self.transaction.description)


class Word_to_Category(models.Model):
    category = models.ForeignKey('Category')
    word = models.CharField('תיאור', max_length=100)

    def __unicode__(self):
        return "%s - %s" % (self.category.name, self.word)

    #def __str__(self):
    #    return unicode(self).encode('utf-8')


class Excluded_Category(models.Model):
    category = models.ForeignKey('Category')
    action = models.ForeignKey('Excluded_Action')

    def __unicode__(self):
        return "%s - %s" % (self.category.name, self.action.action)


class Excluded_Action(models.Model):
    action = models.CharField('פעולה', max_length=30)

    def __unicode__(self):
        return self.action
