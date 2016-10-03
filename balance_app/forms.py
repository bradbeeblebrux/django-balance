# -*- coding: utf-8 -*-

from django import forms
from models import Account, Owner, Category, Word_to_Category


class AddFromFileForm(forms.Form):
    owner = forms.ModelChoiceField(queryset=Owner.objects.all(),
                                   required=True, label='בעל חשבון')
    account = forms.ModelChoiceField(queryset=Account.objects.all(),
                                     required=True, label='חשבון')
    file = forms.FileField(required=True, label='קובץ')


class PreviewTransForm(forms.Form):
    def __init__(self, *args, **kwargs):
        upload_trans_list = kwargs.pop('list')

        super(PreviewTransForm, self).__init__(*args, **kwargs)
        all_categories = Category.objects.all().order_by('name')
        all_words = Word_to_Category.objects.all()

        for i, trans in enumerate(upload_trans_list):
            self.fields['comment_%s' % i] = forms.CharField(required=False)

            selected_category = None
            for www in all_words:
                if trans['desc'] in www.word:
                    selected_category = www.category
                    break
#            try:
#                selected_category = Word_to_Category.objects.filter(
#                    word__contains=trans['desc'])[0].category
#            except (IndexError, Word_to_Category.DoesNotExist):
#                selected_category = None

            self.fields['category_%s' % i] = forms.ModelChoiceField(
                queryset=all_categories,
                required=True,
                initial=selected_category, )
