from django.conf.urls import url
import Balance.views

urlpatterns = [
    url(r'^$', Balance.views.IndexView.as_view(), name='index'),
    url(r'^transaction/all$', Balance.views.transall, name='transall'),
    url(r'^transaction/add_from_file$', Balance.views.trans_add_from_file, name='load_from_file'),
    url(r'^transaction/preview_trans/(?P<key>preview\d+)/$', Balance.views.PreviewTransView, name='preview_trans'),
    url(r'^transaction/summary$', Balance.views.SummaryCategoryView, name='SummaryCategoryView'),
    url(r'^transaction/summary/(?P<year>[0-9]{4})/$', Balance.views.SummaryCategoryView, name='SummaryCategoryView'),
    url(r'^transaction/summary/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', Balance.views.SummaryCategoryView, name='SummaryCategoryView'),
#    url(r'/(?P<trans_id>\d+)/$', 'Balance.views.trans', name='trans'),
#    url(r'^transaction/all$', views.TransAllListView.as_view(), name='transall'),
    url(r'^transaction/list$', Balance.views.AccountListView.as_view(), name='account-list'),
    url(r'^transaction/pie$', Balance.views.SummaryCategoryPieChart),
    url(r'^transaction/pie/(?P<year>[0-9]{4})/$', Balance.views.SummaryCategoryPieChart),
    url(r'^transaction/pie/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', Balance.views.SummaryCategoryPieChart),

]
