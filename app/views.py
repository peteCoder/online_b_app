import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .models import Account, Transaction, Loan, Card, Transfer

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
import json
from django.db.models import Sum, Count
from django.utils import timezone
from collections import defaultdict
import calendar
from django.db.models.functions import ExtractMonth

from django.http import Http404

from .forms import TransferForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignupForm





User = get_user_model()

def get_monthly_transactions(account_type, year, user):
    transactions = Transaction.objects.filter(
        from_account__account_type=account_type,
        from_account__customer=user,
        timestamp__year=year
    ).annotate(month=ExtractMonth('timestamp')).values('month').annotate(total=Sum('amount')).order_by('month')

    monthly_data = defaultdict(lambda: 0)  # Default to 0 if no data for a month
    for transaction in transactions:
        monthly_data[transaction['month']] = transaction['total']

    # Return data as list of amounts for each month
    return [int(monthly_data[month]) for month in range(1, 13)]





# Create your views here.
def home(request):
    # user = User.objects.filter(email=request.user.email).first()
    # print(user.email)

    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    

    # profile = Profile.objects.get(user=request.user)

    accounts = Account.objects.filter(customer=user).all()
    loans = Loan.objects.filter(customer=user)


    account_model_meta = {
        'model_name': Account._meta.model_name.upper(),  # Account model name
    }
    loan_model_meta = {
        'model_name': Loan._meta.model_name.upper(),  # Loan model name
    }



    has_loan = loans.count() > 0

    current_year = timezone.now().year

    checking_data = get_monthly_transactions('CHECKING', current_year, user)
    savings_data = get_monthly_transactions('SAVINGS', current_year, user)
    months_data = list(calendar.month_abbr[1:])

    all_transactions = Transaction.objects.all()

    

    return render(request, "dashboard/major/index.html", {

        'accounts': accounts,
        "loan": loans.first(),
        "has_loan": has_loan,

        # Labels
        "account_model_meta": account_model_meta,
        "loan_model_meta": loan_model_meta,

        'checking_data': json.dumps(checking_data),
        'savings_data': json.dumps(savings_data),
        'months_data': json.dumps(months_data),


    })


@login_required
def LogoutView(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('login')


def main_home(request):
    accounts = Account.objects.all()

    account_model_meta = {
        'model_name': Account._meta.model_name,  # Account model name
        'app_label': Account._meta.app_label,    # App name
    }

    return render(request, "main/index.html", {
        'accounts': accounts,
        "account_model_meta": account_model_meta,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard_home')  # Change to your dashboard page
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, "main/pages-sign-in.html", {})



def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")
    

    
    if request.method == 'POST':
        print(request.POST)  # Print the POST data to confirm what's being submitted
        print(request.FILES)
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            # This will print the actual form validation errors to the terminal

            for field in form:
                print(f"{field.name}: {field.errors}")  # Print specific field errors
            print("Form is not valid")
            print(form.errors)  # Prints field-specific errors
            print(form.non_field_errors())  # Prints non-field errors if any
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = SignupForm()

    return render(request, "main/pages-sign-up.html", {'form': form})




@login_required
def chartpage(request):
    return render(request, "dashboard/major/charts-chartjs.html", {})

@login_required
def transactions(request):
    transaction_records = Transaction.objects.all()
    return render(request, "dashboard/major/transactions.html", {"transactions": transaction_records})

@login_required
def transfer_funds(request):
    transaction_records = Transaction.objects.all()
    accounts = Account.objects.filter(customer=request.user)
    
    
    return render(request, "dashboard/major/transfer_funds.html", {'accounts': accounts})


@csrf_exempt
def validate_transfer(request):
    if request.method == 'POST':
        from_account_id = request.POST.get('from_account')
        amount = request.POST.get('amount')
        to_account = request.POST.get('to_account')

        # Get the account and validate the balance
        try:
            from_account = Account.objects.get(id=from_account_id)
            if from_account.balance < float(amount):
                return JsonResponse({"success": False, "message": "Insufficient funds in the selected account."})
        except Account.DoesNotExist:
            return JsonResponse({"success": False, "message": "Selected account does not exist."})

        # Validate other details (like the existence of the to_account)
        # This is just an example, you'd implement your own logic for validating the recipient's account

        return JsonResponse({"success": True, "message": "Enter your Password"})
    return JsonResponse({"success": False, "message": "Invalid request."})


@csrf_exempt
def confirm_transfer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user

        # Validate password
        password = data.get('password')
        if not authenticate(username=user.email, password=password):
            return JsonResponse({"success": False, "message": "Invalid password."})

        # Process the transfer
        from_account = Account.objects.get(id=data.get('from_account'))
        amount = int(data.get('amount'))

        if from_account.balance < amount:
            return JsonResponse({"success": False, "message": "Insufficient funds."})

        # Deduct the amount from the sender's account
        from_account.balance -= amount
        from_account.save()

        # You'd also want to add code to credit the recipient's account

        # Log the transfer
        Transfer.objects.create(
            user=user,
            from_account=from_account,
            account_holder_name=data.get('beneficiary_name'),
            account_number=data.get('to_account'),
            ach_routing=data.get('ach_routing'),
            account_type=from_account.account_type,
            bank_name=data.get('bank_name'),
            amount=amount,
            address=data.get('address')
        )

        Transaction.objects.create(
            user=request.user,
            transaction_type="TRANSFER",
            from_account=from_account,
            amount=amount,
        )

        return JsonResponse({"success": True, "message": "Transfer successful."})

    return JsonResponse({"success": False, "message": "Invalid request."})

@login_required
def loans(request):
    return render(request, "dashboard/major/loan.html", {})


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    # if request.method == "POST":
    #     # Get user profile data from the request
    #     first_name = request.POST.get("first_name")
    #     last_name = request.POST.get("last_name")
    #     phone_number = request.POST.get("phone_number")
    #     street_address = request.POST.get("street_address")
    #     city = request.POST.get("city")
    #     state = request.POST.get("state")
    #     postal_code = request.POST.get("postal_code")

    #     # Update the user's information
    #     user = request.user
    #     user.first_name = first_name
    #     user.last_name = last_name
    #     user.phone_number = phone_number
    #     user.address = street_address
    #     user.city = city
    #     user.state = state
    #     user.postal_code = postal_code
    #     user.save()

    #     return JsonResponse({"message": "Profile updated successfully"}, status=200)
    return render(request, "dashboard/major/profile.html", {})


@login_required
def update_personal_info(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')
        user.save()
        return JsonResponse({'message': 'Personal information updated successfully.'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)


@login_required
def update_address_info(request):
    if request.method == 'POST':
        user = request.user
        user.address = request.POST.get('street_address')
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        user.postal_code = request.POST.get('postal_code')
        user.save()
        return JsonResponse({'message': 'Address updated successfully.'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

@login_required
def update_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            return JsonResponse({'error': 'New passwords do not match.'}, status=400)
        
        if not request.user.check_password(old_password):
            return JsonResponse({'error': 'Current password is incorrect.'}, status=400)
        
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Prevents logging out after password change
        return JsonResponse({'message': 'Password updated successfully.'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

@login_required
def support_page(request):
    return render(request, "dashboard/major/support_page.html", {})

@login_required
def account_details(request, pk):
    user = request.user
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        raise Http404
    
    transactions = Transaction.objects.filter(from_account=account, user=user)

    return render(
        request, 
        "dashboard/major/account_details.html", 
        {
            "account": account, 
            "transactions": transactions
        }
    )


@login_required
def accounts_list(request):

    accounts = Account.objects.all()

    account_count = accounts.count()

    return render(request, "dashboard/major/account_list.html", {"accounts": accounts, 'account_count': account_count})


@login_required
def create_bank_account(request):
    user = request.user
    existing_account_types = Account.objects.filter(customer=user).values_list('account_type', flat=True)
    account_types_to_create = [
        ('CHECKING', 'Checking'),
        ('SAVINGS', 'Savings'),
        ('MONEY MARKET', 'Money Market'),
        ('CD', 'Certificate of Deposit (CD)'),
    ]

    if request.method == "POST":
        selected_account_type = request.POST.get("account_type")

        if selected_account_type in existing_account_types:
            messages.warning(request, f"You already have a {selected_account_type} account.")
            return redirect('create_account')

        account = Account(
            customer=user,
            account_type=selected_account_type,
        )

        # Handle user-specific inputs for different account types
        if selected_account_type == "SAVINGS":
            account.yearly_income = request.POST.get("yearly_income")
            account.proof_of_funds = request.FILES.get("proof_of_funds")
            account.id_card_front = request.FILES.get("id_card_front")
            account.id_card_back = request.FILES.get("id_card_back")
            account.credit_card_image = request.FILES.get("credit_card_image")
            account.minimum_balance = 1000  # Assigned by the bank

        elif selected_account_type == "MONEY MARKET":
            account.initial_balance = request.POST.get("initial_balance")
            account.proof_of_employment = request.FILES.get("proof_of_employment")
            account.utility_bill = request.FILES.get("utility_bill")
            account.transaction_limit = 10  # Assigned by the bank

        elif selected_account_type == "CD":
            account.deposit_amount = request.POST.get("deposit_amount")
            account.beneficiary_name = request.POST.get("beneficiary_name")
            account.beneficiary_id_proof = request.FILES.get("beneficiary_id_proof")
            account.term_length = 12  # Assigned by the bank

        elif selected_account_type == "CHECKING":
            account.initial_deposit = request.POST.get("initial_deposit")
            account.overdraft_protection = request.POST.get("overdraft_protection") == 'on'
            account.id_card = request.FILES.get("id_card")

        account.save()

        messages.success(request, f"{account.get_account_type_display()} account created successfully.")
        return redirect('accounts')

    return render(request, "dashboard/major/create_account.html", {
        'existing_account_types': existing_account_types,
        'account_types_to_create': account_types_to_create,
    })


@login_required
def confirm_account_activation_payment(request, pk):
    account = Account.objects.get(id=pk)
    
    if request.method == 'POST':
        receipt = request.FILES.get('receipt')
        
        if receipt:
            # Assuming you have a field for the receipt in the Card model
            account.activation_receipt = receipt
            account.applied_for_activation = True
            account.save()
            
            messages.success(request, 'Payment confirmed! Your account will be activated soon.')
        else:
            messages.error(request, 'Please upload a valid receipt.')
        
        return redirect('accounts_detail', pk=account.id)

    return render(request, 'dashboard/major/create_account.html', {'account': account})


@login_required
def card_list(request):
    cards = Card.objects.filter(user=request.user)
    return render(request, 'dashboard/major/card_list.html', {'cards': cards})

@login_required
def card_detail(request, pk):
    card = Card.objects.get(pk=pk)
    return render(request, 'dashboard/major/card_detail.html', {'card': card})


@login_required
def confirm_card_payment(request, pk):
    card = Card.objects.get(id=pk)
    
    if request.method == 'POST':
        receipt = request.FILES.get('receipt')
        
        if receipt:
            # Assuming you have a field for the receipt in the Card model
            card.confirmation_receipt = receipt
            card.applied_for_activation = True
            card.save()
            
            messages.success(request, 'Payment confirmed! Your card will be activated soon.')
        else:
            messages.error(request, 'Please upload a valid receipt.')
        
        return redirect('card_detail', pk=card.id)

    return render(request, 'dashboard/major/create_card.html', {'card': card})


@login_required
def create_card(request):
    # Get the types of cards the user hasn't created yet
    existing_card_types = Card.objects.filter(user=request.user).values_list('card_type', flat=True)
    available_card_types = [card for card in ['MasterCard', 'Verve', 'Visa'] if card not in existing_card_types]

    if request.method == 'POST':
        card_type = request.POST.get('card_type')

        # Check if the user already has a card of this type
        if Card.objects.filter(user=request.user, card_type=card_type).exists():
            return JsonResponse({'error': f'You already have a {card_type} card.'}, status=400)

        # If the user doesn't have this card type, create a new one
        card = Card(user=request.user, card_type=card_type)
        card.generate_card_number()
        card.generate_cvv()
        card.generate_expiration_date()
        card.generate_fee_for_card()
        card.save()

        return JsonResponse({'message': 'Card created successfully!', 'card_id': card.id})
    

    return render(request, 'dashboard/major/create_card.html', {'available_card_types': available_card_types})