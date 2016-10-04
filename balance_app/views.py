# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import encoding
from .models import Transaction, Owner, Account, Transaction_to_Category, Word_to_Category, Category, Excluded_Category
from .forms import AddFromFileForm, PreviewTransForm
import json
import datetime
import accounts
import random
import pdb



def dashboard(request):
	return render(request, "balance_app/dashboard.html")

def transall(request):
    return render(request, "balance_app/transall.html", {"trans": Transaction.objects.all()})


def SummaryCategoryView(request, year=None, month=None):

    summary = {cat: 0 for cat in Category.get_categories()}
    _summary = Transaction_to_Category.objects
    total = 0

    if year is not None:
        _summary = _summary.filter(transaction__charge_date__year=year)

    if month is not None:
        _summary = _summary.filter(transaction__charge_date__month=month)

    _summary = _summary.values('category__id', 'category__name').annotate(total=Sum('transaction__amount'))
    for t in _summary:
        total += t['total']
        summary[t['category__name']] = t['total']

    return render(request, "balance_app/summary.html", {"total": total, "summary": summary})

def SummaryCategoryPieChart(request, year=None, month=None):

    summary = {cat: 0 for cat in Category.get_categories()}
    _summary = Transaction_to_Category.objects.all()

    if year is not None:
        _summary = _summary.filter(transaction__charge_date__year=year)

    if month is not None:
        _summary = _summary.filter(transaction__charge_date__month=month)

    _summary = _summary.values('category__id', 'category__name').annotate(total=Sum('transaction__amount'))
    for t in _summary:
        summary[t['category__name']] = abs(t['total'])

    return render(request, "balance_app/summary_pie.html", {"summary": summary})


def trans(request, trans_id):
    trans = get_object_or_404(Transaction, pk=trans_id)
    return render_to_response('balance_app/trans.html', {'trans': trans})

#    transaction = Transactions.objects.filter(id=trans_id).values()
#    response = HttpResponse("", content_type="text/html; charset=utf-8")
#    response.write('<html><body>')
#    response.write(transaction)
#    response.write('</body></html>')
#    return response


def handle_uploaded_file(filename, account_name):
    acc = Account.objects.filter(name=account_name)
    if len(acc) == 1:
        parserFunc = getattr(accounts, acc[0]._class)
        return parserFunc(filename)
    else:
        return []


#for debugging import pdb; pdb.set_trace()
def PreviewTransView(request, key):
    upload_list_str = request.session.get(key)
    upload_dict = json.loads(upload_list_str)
    owner = upload_dict['owner']
    account = upload_dict['account']
    upload_list_obj = upload_dict['transactions']

    form = PreviewTransForm(request.POST or None, **{'list': upload_list_obj})

    for index in range(0, len(upload_list_obj)):
        upload_list_obj[index]['comment'] = form['comment_' + str(index)]
        upload_list_obj[index]['category'] = form['category_' + str(index)]

    if form.is_valid():
            # return HttpResponseRedirect('/thanks/') # Redirect after POST

        # clean_data.items are returned as a list for items without any order
        # we need to aggregate the transactions with the same index
        for item, value in form.cleaned_data.items():
            field_name, index = item.split("_")
            upload_list_obj[int(index)][field_name] = value

        temp = ""
        temp_cat = ""
        temp_word = ""
        for item in upload_list_obj:

            if Excluded_Category.objects.filter(category=item['category']):
                continue

            trans, created = Transaction.objects.get_or_create(
                date=item['date'],
                charge_date=item['charge_date'],
                reference=item['reference'],
                description=item['desc'],
                amount=item['amount'],
                comment=item['comment'],
                owner=Owner.objects.get(id=owner),
                account=Account.objects.get(id=account))
            temp += "%s created: %s<br>\n" % (trans, created)

            trans_to_cat, created = Transaction_to_Category.objects.get_or_create(
                category=item['category'],
                transaction=trans)
            temp_cat += "%s created: %s<br>\n" % (trans_to_cat, created)

            word_to_cat, created = Word_to_Category.objects.get_or_create(
                category=item['category'],
                word=item['desc'])
            temp_word += "%s created: %s<br>\n" % (word_to_cat, created)


        temp = "{0}</br></br>{1}</br></br>{2}".format(temp, temp_cat, temp_word)
        response = HttpResponse(temp, content_type="text/html; charset=utf-8")
            # response.write(upload_response)
        return response

    return render(request, 'balance_app/preview_trans.html', {'form': form, 'temp_list': upload_list_obj, 'key': key})


def trans_add_from_file(request):
    if request.method == 'POST':
        form = AddFromFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_trans_dict = handle_uploaded_file(request.FILES['file'], form.cleaned_data['account'].name)

            dict_to_serialize = {'owner': form.cleaned_data['owner'].id,
                                 'account': form.cleaned_data['account'].id,
                                 'transactions': [ob.__dict__ for ob in upload_trans_dict]}
            json_string = json.dumps(dict_to_serialize)

            key = 'preview%s' % random.randint(0, 999999)
            request.session[key] = json_string

            return redirect('balance_app:preview_trans', key)
    else:
        form = AddFromFileForm()

    return render(request, 'balance_app/add_from_file.html', {'form': form, })



#return HttpResponseRedirect(reverse('balance:preview_trans'))
# return HttpResponseRedirect('/thanks/') # Redirect after POST
# response = HttpResponse("", content_type="text/html; charset=utf-8")
# response.write(upload_response)
# return response
#json_string = json.dumps([ob.__dict__ for ob in upload_trans_dict], encoding="utf-8")

from django.views.generic.list import ListView


class AccountListView(ListView):

    model = Account

    def get_context_data(self, **kwargs):
        context = super(AccountListView, self).get_context_data(**kwargs)
        return context
