from django.test import TestCase
from .models import Client, Loan, Payment
from datetime import date
from freezegun import freeze_time

class LoanTestCase(TestCase):

    @freeze_time("2023-12-12")
    def setUp(self):
        # Creating a client
        self.client = Client.objects.create(
            full_name="John Doe",
            CNIC="1234567890123",
            address="123 Main St",
            phone="1234567890",
            email="john.doe@example.com"
        )

        # Creating a loan
        self.loan = Loan.objects.create(
            client=self.client,
            loan_amount=1000,
            interest_rate=5,
            start_date="2023-11-01",  # Set loan start date
            Loan_Duration=12  # 12 months loan duration
        )

        # Making a payment
        self.payment = Payment.objects.create(
            client=self.client,
            loan=self.loan,
            amount_paid=100,
            paid_date="2024-02-01"
        )

    def test_total_payment(self):
        # Total payment should be loan amount + interest
        self.assertEqual(self.loan.Total_Payment, 1050)

    def test_remaining_amount(self):
        # Remaining amount should be Total_Payment - amount_paid
        self.assertEqual(self.loan.remaining_amount, 950.00)

    def test_installment(self):
        # Installment should be Total_Payment divided by Loan_Duration
        self.assertEqual(self.loan.Installment, 87.5)

    def test_payment_status(self):
        # Test if payment status is 'Pending' before due date
        self.assertEqual(self.loan.Payment_status, 'Pending')

    def test_payment_status_after_due(self):
        # Freeze time to 2024-11-11 to check for overdue status
        # We assume the loan started 12 months before, so it should be overdue
        self.assertEqual(self.loan.Payment_status, 'Overdue')

    def test_next_payment_date(self):
        # The next payment date should be one month after the start date
        self.assertEqual(self.loan.next_payment_date, date(2023, 12, 1))

    def test_loan_str_method(self):
        # Check string representation of Loan
        self.assertEqual(str(self.loan), "Loan 1 for John Doe")

    def test_payment_str_method(self):
        # Check string representation of Payment
        self.assertEqual(str(self.payment), "Payment 1 for Loan 1")
