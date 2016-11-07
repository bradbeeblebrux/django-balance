# -*- coding: utf-8 -*-
from .models import Transaction, Account, Owner, Transaction_to_Category
import datetime
from django.core import serializers
import json
from elasticsearch import Elasticsearch
import pdb


def index_all_dirty():
	num_of_records = 0
	list_of_accounts = Account.objects.all()
	list_of_owners = Owner.objects.all()
	es = Elasticsearch()
	qs = Transaction.objects.filter(dirty=True)
	for t in qs:
		idx = es_index_name(t)
		if getattr(t,'_id',None) is not None: # we will delete the index
			try:
				es.delete(index=idx, doc_type='transaction', id=t._id)	
			except Exception:
				pass
		t.category = Transaction_to_Category.objects.get(id=t.id).category.name
		body = serialize_model(t,list_of_accounts,list_of_owners)
		res = es.index(index=idx, doc_type='transaction', body=body)
		if res['created']:
			t.dirty = False
			t._id = res['_id']
			t.save()
			num_of_records += 1
	print "updated " + str(num_of_records) + " records"
			

# generate es index name out of the tarnsaction date
def es_index_name(transaction):
	tr_date = transaction.charge_date
	date_stamp = tr_date.strftime('%Y-%m')
	return "transactions-" + date_stamp

# serialize the transaction into a JSON obj for indexing
def serialize_model(transaction, accounts, owners):
	data = serializers.serialize('json', [transaction,])
	struct = json.loads(data)
	obj = struct[0]['fields']
	del obj['_id']
	del obj['dirty']
	obj['category'] = transaction.category
	obj['account'] = accounts.get(id=transaction.account.id).name
	obj['owner'] = owners.get(id=transaction.owner.id).name
	obj['amount'] = float(obj['amount'])
	return json.dumps(obj)



