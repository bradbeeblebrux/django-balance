from django.conf.urls import url

from . import views

app_name = 'balance_app'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^transaction/all$', views.transall, name='transall'),
    url(r'^transaction/add_from_file$', views.trans_add_from_file, name='load_from_file'),
    url(r'^transaction/preview_trans/(?P<key>preview\d+)/$', views.PreviewTransView, name='preview_trans'),
    url(r'^transaction/summary$', views.SummaryCategoryView, name='SummaryCategoryView'),
    url(r'^transaction/summary/(?P<year>[0-9]{4})/$', views.SummaryCategoryView, name='SummaryCategoryView'),
    url(r'^transaction/summary/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.SummaryCategoryView, name='SummaryCategoryView'),
#    url(r'/(?P<trans_id>\d+)/$', 'views.trans', name='trans'),
#    url(r'^transaction/all$', views.TransAllListView.as_view(), name='transall'),
#    url(r'^transaction/list$', views.AccountListView.as_view(), name='account-list'),
    url(r'^transaction/pie$', views.SummaryCategoryPieChart),
    url(r'^transaction/pie/(?P<year>[0-9]{4})/$', views.SummaryCategoryPieChart),
    url(r'^transaction/pie/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.SummaryCategoryPieChart),

]
