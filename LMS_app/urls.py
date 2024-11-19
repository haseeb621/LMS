from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('search_client',search_client,name='search_client'),
    path('pay_installment/<int:id>',pay_installment,name='pay_installment'),
    path('process_payment/<int:id>',process_payment,name='process_payment'),
    path('payment_info/<int:id>',payment_info,name='payment_info'),
    path('payment_success/<int:payment_id>',payment_success,name='payment_success'),
    path('reverse_client_info/<int:client_CNIC>',reverse_client_info,name='reverse_client_info'),
]
