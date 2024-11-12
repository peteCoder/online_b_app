from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import random
from datetime import datetime, timedelta

import string
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the bank app where email is the unique identifier for authentication.
    """

    EMPLOYMENT_STATUS = [
        ("employed", "employed"),
        ("self-employed", "self-employed"),
        ("unemployed", "unemployed"),
    ]
    PREFERRED_ACCOUNT_TYPE = [
        ('CHECKING', 'Checking'),
        ('SAVINGS', 'Savings'),
        ('MONEY_MARKET', 'Money Market'),
        ('CD', 'Certificate of Deposit (CD)'),
    ]

    otp_code =  models.CharField(max_length=100, blank=True, null=True)

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=False)  # Required
    last_name = models.CharField(max_length=50, blank=False)   # Required
    phone_number = models.CharField(max_length=15, unique=True, blank=False)  # Required
    
    ssn = models.CharField(max_length=50, blank=False)  # Required

    bank_id = models.CharField(max_length=10, unique=True, blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)
    annual_income = models.CharField(max_length=100, blank=True, null=True)
    employment_status = models.CharField(max_length=100, choices=EMPLOYMENT_STATUS, blank=True, null=True)
    preferred_account_type = models.CharField(max_length=100, choices=PREFERRED_ACCOUNT_TYPE, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile/images", blank=True, null=True)


    address = models.TextField(blank=True, null=True)  # Required
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    



    front_id_image = models.ImageField(upload_to="identity/images", blank=True, null=True)
    back_id_image = models.ImageField(upload_to="identity/images", blank=True, null=True)





    
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    @property
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            # Change this later
            return 'http://localhost:8000/static/static/img/avatars/avatar-5.jpg'
        
    @property
    def get_user_fullname(self):
        return str(self.first_name).capitalize() + " " + str(self.last_name).capitalize()


    def __str__(self):
        return self.email
    
    @property
    def get_total_amount_in_account(self):
        # User account balance
        accounts = self.account_set.all()
        subtotal = 0
        for acc in accounts:
            subtotal += acc.balance
        return subtotal
    
    class Meta:
        verbose_name_plural = "Users"
        verbose_name = "User"


# Signal to generate a unique bank_id after user creation
@receiver(post_save, sender=CustomUser)
def generate_unique_bank_id(sender, instance, created, **kwargs):
    if created and not instance.bank_id:
        while True:
            random_id = ''.join(random.choices(string.digits, k=10))
            if not CustomUser.objects.filter(bank_id=random_id).exists():
                instance.bank_id = random_id
                instance.save()
                break



def change_account_location():
    ACCOUNT_LOCATIONS = [
        "1475 Huntington Drive Duarte, California 91010",
        "2171 SE Federal Highway Stuart, Florida 34994",
        "2171 SE Federal Highway Stuart, Florida 34994",
        "2775 Buford Highway Duluth, GA 30096",
        "2775 Buford Highway Duluth, GA 30096",
        "128 Loyola Drive Myrtle Beach, SC 29588",
        "4040 River Oaks Drive Myrtle Beach, SC 29579",
    ]
    location = random.choice(ACCOUNT_LOCATIONS)
    return location

def generate_ach_routing():
    """Auto-generate a random ACH routing number."""
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

def generate_account_number():
    """Auto-generate a random 10-digit account number."""
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('CHECKING', 'Checking'),
        ('SAVINGS', 'Savings'),
        ('MONEY MARKET', 'Money Market'),
        ('CD', 'Certificate of Deposit (CD)'),
    )

    # Required fields
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100, unique=True, default=generate_account_number)
    account_type = models.CharField(max_length=40, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True, default="FirstCitzen Bank")
    location = models.CharField(max_length=500, blank=True, null=True, default=change_account_location)
    ach_routing = models.CharField(max_length=9, blank=True, null=True, default=generate_ach_routing)


     # Shared fields
    id_card_front = models.ImageField(upload_to='id_cards/', null=True, blank=True)
    id_card_back = models.ImageField(upload_to='id_cards/', null=True, blank=True)

    # Savings account-specific fields
    yearly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    proof_of_funds = models.FileField(upload_to='proof_of_funds/', null=True, blank=True)
    credit_card_image = models.ImageField(upload_to='credit_cards/', null=True, blank=True)

    # Money Market account-specific fields
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    proof_of_employment = models.FileField(upload_to='employment_proofs/', null=True, blank=True)
    utility_bill = models.FileField(upload_to='utility_bills/', null=True, blank=True)

    # CD account-specific fields
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    beneficiary_name = models.CharField(max_length=255, null=True, blank=True)
    beneficiary_id_proof = models.FileField(upload_to='beneficiary_id_proofs/', null=True, blank=True)
    term_length = models.IntegerField(null=True, blank=True, help_text="Term length in months")

    # Checking account-specific fields
    initial_deposit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    overdraft_protection = models.BooleanField(default=False)

    confirmation_payment_amount = models.IntegerField(default=100)
    transaction_limit = models.IntegerField(default=1000)


    # proof_of_income = models.ImageField(upload_to='proof-of-income/', null=True, blank=True)
    activation_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    activated = models.BooleanField(default=False)
    applied_for_activation = models.BooleanField(default=False)


    def generate_confirmation_payment_amount(self, initial_deposit):
        if self.account_type == "CHECKING":
            self.confirmation_payment_amount = 200
        elif self.account_type == "SAVINGS":
            if int(initial_deposit) > 100:
                self.confirmation_payment_amount = int(initial_deposit)
            self.confirmation_payment_amount = 100
        else:
            self.confirmation_payment_amount = 300

    def __str__(self):
        return f"{self.customer.email} - {self.account_type} ({self.account_number})"

    class Meta:
        verbose_name_plural = "Accounts"
        verbose_name = "Account"



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'DEPOSIT'),
        ('WITHDRAWAL', 'WITHDRAWAL'),
        ('TRANSFER', 'TRANSFER'),
    )

    TRANSACTION_STATUS = [
        ("Pending", "Pending"),
        ("Successful", "Successful")
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    from_account = models.ForeignKey(Account, related_name='from_transactions', on_delete=models.SET_NULL, null=True, blank=True)
    to_account = models.ForeignKey(Account, related_name='to_transactions', on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='Pending')

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} from {self.from_account.account_number}"
    
    class Meta:
        verbose_name_plural = "Transactions"
        verbose_name = "Transaction"



class Card(models.Model):

    CARD_TYPES = [
        ('MasterCard', 'MasterCard'),
        ('Verve', 'Verve'),
        ('Visa', 'Visa')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=200, blank=True, null=True)
    card_type = models.CharField(max_length=200, blank=True, null=True)
    cvv = models.CharField(max_length=30, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    name_in_card = models.CharField(max_length=200, blank=True, null=True)
    is_real_card = models.BooleanField(default=False)
    month_and_year_of_expiration = models.CharField(max_length=100, blank=True, null=True)

    confirmation_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)

    activated = models.BooleanField(default=False)
    card_activation_fee = models.IntegerField(default=100)
    applied_for_activation = models.BooleanField(default=False)
    card_expiration = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_card_number(self):
        """Generate card number based on card type"""
        if self.card_type == 'MasterCard':
            prefix = "5555"
        elif self.card_type == 'Verve':
            prefix = "5061"
        elif self.card_type == 'Visa':
            prefix = "4111"
        else:
            prefix = "0000"  # Default if something goes wrong

        # Generate the rest of the card number randomly
        rest_of_card_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        self.card_number = prefix + rest_of_card_number

    def generate_fee_for_card(self):
        """Generate a fee for card activation"""
        if self.card_type == "Verve":
            self.card_activation_fee = 40
        elif self.card_type == "MasterCard":
            self.card_activation_fee = 60
        elif self.card_type == "Visa":
            self.card_activation_fee = 90
        else:
            self.card_activation_fee = 100


    def generate_cvv(self):
        """Generate a 3-digit random CVV"""
        self.cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])

    def generate_expiration_date(self):
        """Set the expiration date to 4 years from now"""
        self.expiration_date = datetime.now() + timedelta(days=4*365)

    def __str__(self):
        return f"{self.user.email} - {self.card_type}"
    
    class Meta:
        verbose_name_plural = "Cards"
        verbose_name = "Card"

class Loan(models.Model):
    LOAN_TYPES = [
        ('personal', 'Personal Loan'),
        ('mortgage', 'Mortgage'),
        ('auto', 'Auto Loan'),
        ('business', 'Business Loan')
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=200, choices=LOAN_TYPES, blank=False, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_term = models.IntegerField(default=12)  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)  # 10% interest rate
    interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # interest calculated based on formula
    repayment_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # total repayable amount
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)

    activation_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    activated = models.BooleanField(default=False)
    applied_for_activation = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        self.interest = (float(self.amount) * float(self.interest_rate) * float(self.loan_term)) / 100
        self.repayment_amount = float(self.amount) + float(self.interest)
        self.due_date = timezone.now() + timedelta(days=int(self.loan_term) * 30)  # approx. due in months
        super().save(*args, **kwargs)
 
    def __str__(self):
        return f"Loan for {self.customer.email} - {self.amount}"
    
    class Meta:
        verbose_name_plural = "Loans"
        verbose_name = "Loan"


class Transfer(models.Model):
    ACCOUNT_TYPES = (
        ('CHECKING', 'Checking'),
        ('SAVINGS', 'Savings'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    from_account = models.ForeignKey(Account, related_name='transfered_from', on_delete=models.CASCADE)
    
    account_holder_name = models.CharField(max_length=200, blank=True, null=True)
    account_number = models.CharField(max_length=200, blank=True, null=True)
    ach_routing = models.CharField(max_length=200, blank=True, null=True)
    account_type = models.CharField(max_length=200, choices=ACCOUNT_TYPES, blank=True, null=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)


    def __str__(self):
        return f"Transfer for {self.user.email} - {self.amount}"
    
    class Meta:
        verbose_name_plural = "Transfer"
        verbose_name = "Transfer"



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.title}"

    class Meta:
        verbose_name_plural = "Notification"
        verbose_name = "Notifications"


class Support(models.Model):
    STATUS = [
        ("Pending", "Pending"),
        ("Fulfilled", "Fulfilled"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=400, blank=True, null=False)
    description = models.TextField(max_length=400, blank=True, null=False)
    image = models.FileField(upload_to='support/images/', null=True, blank=True)
    status = models.CharField(max_length=400, blank=True, null=False, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Support"
        verbose_name = "Support"

    def __str__(self):
        return f"Support for {self.user.email} - {self.subject}"


class Payment(models.Model):
    TRANSACTION_TYPE = [
        ("transfer", "transfer"),
        ("withdrawal", "withdrawal"),
        ("deposit", "deposit"),
    ]
    PAYMENT_METHOD = [
        ("bank", "bank"),
        ("crypto", "crypto"),
        ("paypal", "paypal"),
        ("cashapp", "cashapp"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=400, blank=True, null=False, choices=TRANSACTION_TYPE)
    confirmation_receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    payment_method = models.CharField(max_length=400, blank=True, null=False, choices=PAYMENT_METHOD)
    is_tax = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self) -> str:
        return f"Received Payment from {self.user.email} in {self.payment_method}"






