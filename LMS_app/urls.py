from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('search_client',search_client,name='search_client'),
    path('pay_installment/<int:id>',pay_installment,name='pay_installment'),
    path('process_payment/<int:id>',process_payment,name='process_payment'),
    path('payment_success/<int:payment_id>',payment_success,name='payment_success'),
]