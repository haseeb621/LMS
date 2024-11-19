from django.shortcuts import get_object_or_404, redirect, render
from .models import *
import datetime
from django.contrib import messages
# Create your views here.
def index(request):
  return render(request,'index.html')
def search_client(request):
  if request.method=='POST':
   client_CNIC=request.POST['client_CNIC']
   client_info=get_object_or_404(Client,CNIC=client_CNIC)
   return render(request,"client_info.html",{'client':client_info,'client_CNIC':client_CNIC})
  return redirect('search_client')
def reverse_client_info(request,client_CNIC):
   client_info=get_object_or_404(Client,CNIC=client_CNIC)
   return render(request,"client_info.html",{'client':client_info,'client_CNIC':client_CNIC})
def payment_info(request,id):
  data=Client.objects.filter(loan=id).first()
  payments=Payment.objects.filter(loan=id)
  return render(request,'payment_info.html',{'payments':payments,'data':data})
def pay_installment(request,id):
  loan=get_object_or_404(Loan,id=id,)
  return render(request,'pay_installment.html',{'loan':loan})
def process_payment(request,id):
  if request.method=='POST':
    amount=int(request.POST['amount'])
    loan=get_object_or_404(Loan,id=id)
    if amount > loan.remaining_amount:
      messages.error(request,"Payment cannot be greater that Remaining Amount")
      return redirect('process_payment',id=loan.id)
    payment=Payment.objects.create(client=loan.client,
                         loan=loan,
                         amount_paid=amount,
                         payment_date=datetime.date.today())
    
    payment.save()
    
    return redirect('payment_success',payment_id=payment.id)
  return redirect('process_payment',{'loan':loan})
def payment_success(request,payment_id):
  payment=get_object_or_404(Payment,id=payment_id)
  return render(request,'payment_success.html',{'payment':payment})