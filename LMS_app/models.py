from django.db import models
from dateutil.relativedelta import relativedelta
import datetime
from decimal import Decimal
class Client(models.Model):
    full_name = models.CharField(max_length=50)
    CNIC = models.CharField(max_length=13)  # Changed to CharField for CNIC
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name

class Loan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    loan_amount = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    Loan_Duration = models.IntegerField(default=12, help_text='In months')
    
    LOAN_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Availed', 'Availed'),
        ('Declined', 'Declined'),
        ('Closed', 'Closed'),
        ('NotApplied', 'Not Applied')
    ]
    loan_status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='NotApplied')

    @property
    def Total_Payment(self):
        return self.loan_amount + (self.loan_amount * (self.interest_rate / 100))

    @property
    def remaining_amount(self):
        total_paid = sum(payment.amount_paid for payment in self.payment_set.all())
        return Decimal(self.Total_Payment - total_paid)

    @property
    def Installment(self):
        return round((self.Total_Payment) / self.Loan_Duration, 2)

    @property
    def Payment_status(self):
     due_date = self.start_date + relativedelta(months=self.Loan_Duration)
     if datetime.date.today() > due_date and self.remaining_amount > 0:
         return 'Overdue'
     return 'Pending'


    @property
    def next_payment_date(self):
        return self.start_date + relativedelta(months=1)
    
    def __str__(self):
        return f"Loan {self.id} for {self.client.full_name}"

class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    paid_date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField for payment amounts
    payment_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.loan.save()  # Consider updating specific fields instead

    def __str__(self):
        return f"Payment {self.id} for Loan {self.loan.id}"
