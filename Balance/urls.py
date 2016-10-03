# from django.conf.urls import url
# import Balance.views

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^balance/', include('balance_app.urls')),
    url(r'^admin/', admin.site.urls),
]
