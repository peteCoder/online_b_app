from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from .helpers import check_email, is_valid_password

from rest_framework.views import APIView

from django.contrib.auth import authenticate, login

from django.shortcuts import render
from app.models import Account, Transaction, Loan, Card

from django.contrib.auth import get_user_model

from django.db.models import Sum, Count
from django.utils import timezone
from collections import defaultdict
import calendar
from django.db.models.functions import ExtractMonth

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models import Support
from .serializers import SupportSerializer, AccountActivationSerializer
from app.models import CustomUser
from django.contrib import messages

from django.conf import settings



User = get_user_model()

class RegisterAPIView(APIView):
    def post(self, request):
        required_fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'ssn',
            'annual_income', 'employment_status', 'preferred_account_type',
            'profile_image', 'front_id_image', 'back_id_image',
            'password', 'password_confirmation'
        ]

        email = request.data.get("email")

        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            return Response({"error": "User with email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for password confirmation match
        if request.data['password'] != request.data['password_confirmation']:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        try:
            user = CustomUser.objects.create_user(
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                email=request.data['email'],
                phone_number=request.data['phone_number'],
                ssn=request.data['ssn'],
                annual_income=request.data['annual_income'],
                employment_status=request.data['employment_status'],
                preferred_account_type=request.data['preferred_account_type'],
                profile_image=request.FILES.get('profile_image'),
                front_id_image=request.FILES.get('front_id_image'),
                back_id_image=request.FILES.get('back_id_image'),
                password=request.data['password']
            )
            # self.send_registration_email(user)
            return Response({"message": "User registered successfully. Check your email for details."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def send_registration_email(self, user):
        subject = "Your Registration Details"
        message = f"Hello {user.get_user_fullname},\n\nYour bank account has been successfully created. Your Bank ID is {user.bank_id} and your password is as you set it during registration.\n\nThank you for joining us!"
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )



@api_view(['POST'])
def login_with_bank_id_api(request):
    bank_id = request.data.get('bank_id')
    password = request.data.get('password')

    # 0656312726

    print(f"Details {bank_id} {password}")

    try:
        user = CustomUser.objects.get(bank_id=bank_id)
        user = authenticate(request, email=user.email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            # Change the redirect url here if you change the dashboard
            return Response({'message': 'Login successful', 'redirect_url': '/'}, status=status.HTTP_200_OK)
        else:
            messages.success(request, "Invalid credentials")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



def get_monthly_transactions(account_type, year, user):
    transactions = Transaction.objects.filter(
        from_account__account_type=account_type,
        timestamp__year=year
    ).annotate(month=ExtractMonth('timestamp')).values('month').annotate(total=Sum('amount')).order_by('month')

    monthly_data = defaultdict(lambda: 0)  # Default to 0 if no data for a month
    for transaction in transactions:
        monthly_data[transaction['month']] = transaction['total']

    # Return data as list of amounts for each month
    return [int(monthly_data[month]) for month in range(1, 13)]



@api_view(['GET'])
def generate_transaction_chart(request):

    current_year = timezone.now().year

    checking_data = get_monthly_transactions('CHECKING', current_year)
    savings_data = get_monthly_transactions('SAVINGS', current_year)

    return Response({
        'checking_data': checking_data,
        'savings_data': savings_data,
        'months': list(calendar.month_abbr[1:]),
    }, status=status.HTTP_200_OK)




# Create your views here.
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        first_name =  request.data.get("first_name")
        last_name =  request.data.get("last_name")
        id_card_front =  request.FILES.get("id_card_front") 
        id_card_back =  request.FILES.get("id_card_back") 
        ssn =  request.data.get("ssn") 
    
        email = request.data.get("email")
        password = request.data.get("password")
        password_confirm = request.data.get("password_confirm")

        if password != password_confirm:
            return Response({
                "detail": "Passwords must match."
            }, status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({
                "detail": "Email is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({
                "detail": "Password is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check if email and password are valid entry
            email_valid_status = check_email(email)
            password_valid_status = is_valid_password(password)

            if password_valid_status.status == False:
                return Response({
                    "detail": "".join([
                        error_message for error_message in password_valid_status.error_messages
                    ])
                }, status=status.HTTP_400_BAD_REQUEST)

            if email_valid_status.status == False:
                return Response({
                    "detail": "".join([
                        error_message for error_message in email_valid_status.error_messages
                    ])
                }, status=status.HTTP_400_BAD_REQUEST)
            
    return Response({"message": "This is working"})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_support_request(request):
    serializer = SupportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ConfirmAccountActivationAPIView(request, pk):

    receipt = request.FILES.get("receipt")
    try:
        account = Account.objects.get(id=pk, customer=request.user)
        print("Account: ", account.id)
    except Account.DoesNotExist:
        return Response({'error': 'Account not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    account.receipt = receipt
    account.applied_for_activation = True
    account.save()
    return Response({'success': 'Payment confirmed! Your account will be activated soon.'}, status=status.HTTP_200_OK)



import json

@api_view(['POST'])
def connect_new_card(request):
    if request.method == 'POST':
    
        data = request.data
        
        card_type = data.get('card_type')
        card_number = data.get('card_number')
        cvv = data.get('cvv')
        name_in_card = data.get('name_in_card')
        card_expiration = data.get('card_expiration')

        print("DATA: ",card_type, card_number, cvv, name_in_card, card_expiration)

        # Check if the user already has a card of this type
        if Card.objects.filter(user=request.user, card_type=card_type).exists():
            return Response({'error': f'You already have a {card_type} card.'}, status=status.HTTP_400_BAD_REQUEST)

        # If the user doesn't have this card type, create a new one
        card = Card.objects.create(
            user=request.user,
            card_type=card_type,
            card_number=card_number,
            cvv=cvv,
            name_in_card=name_in_card,
            card_expiration=card_expiration,
            is_real_card = True,
        )
        
        
        return Response({'message': 'Card created successfully!', 'card_id': card.id}, status=status.HTTP_201_CREATED)
