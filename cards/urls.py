from django.conf.urls import url
from django.contrib import admin

from .views import (
    CardDetailView,
    CardCheckoutView,
    CardNumberValidationView,
    CardPasswordValidationView,
    CardOperationsView,
    CardWithdrawalView,
)

app_name = 'cards'

urlpatterns = [
    url(r'^num/$', CardNumberValidationView.as_view(), name='num_validator'),
    url(r'^pass/$', CardPasswordValidationView.as_view(), name='pass_validator'),
    url(r'^menu/$', CardOperationsView.as_view(), name='menu'),
    url(r'^detail/$', CardDetailView.as_view(), name='detail'),
    url(r'^withdrawal/$', CardWithdrawalView.as_view(), name='withdrawal'),
    url(r'^checkout/$', CardCheckoutView.as_view(), name='checkout'),

]
