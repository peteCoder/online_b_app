from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

import random
from datetime import datetime, timedelta



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


    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=False)  # Required
    last_name = models.CharField(max_length=50, blank=False)   # Required
    phone_number = models.CharField(max_length=15, unique=True, blank=False)  # Required
    address = models.TextField(blank=False)  # Required
    ssn = models.CharField(max_length=50, blank=False)  # Required


    created_at = models.DateTimeField(auto_now_add=True)
    annual_income = models.CharField(max_length=100, blank=True, null=True)
    employment_status = models.CharField(max_length=100, choices=EMPLOYMENT_STATUS, blank=True, null=True)
    preferred_account_type = models.CharField(max_length=100, choices=PREFERRED_ACCOUNT_TYPE, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile/images", blank=True, null=True)
    front_id_image = models.ImageField(upload_to="identity/images", blank=True, null=True)
    back_id_image = models.ImageField(upload_to="identity/images", blank=True, null=True)



    
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

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



class Account(models.Model):
    ACCOUNT_TYPES = (
        ('CHECKING', 'Checking'),
        ('SAVINGS', 'Savings'),
    )

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bank_name = models.CharField(max_length=200, blank=True, null=True, default="FirstCitzen Bank")
    location = models.CharField(max_length=500, blank=True, null=True, default=change_account_location)
    ach_routing = models.CharField(max_length=200, blank=True, null=True)

    
    def __str__(self):
        return f"{self.customer.email} - {self.account_type} ({self.account_number})"

    class Meta:
        verbose_name_plural = "Accounts"
        verbose_name = "Account"



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    from_account = models.ForeignKey(Account, related_name='from_transactions', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='to_transactions', on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

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
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    cvv = models.CharField(max_length=3)
    expiration_date = models.DateField()
    activated = models.BooleanField(default=False)
    applied_for_activation = models.IntegerField(default=100)
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
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    is_paid = models.BooleanField(default=False)

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
        verbose_name_plural = "Transactions"
        verbose_name = "Transaction"


