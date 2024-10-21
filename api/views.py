from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .helpers import check_email, is_valid_password


from django.shortcuts import render
from app.models import Account, Transaction, Loan

from django.contrib.auth import get_user_model

from django.db.models import Sum, Count
from django.utils import timezone
from collections import defaultdict
import calendar
from django.db.models.functions import ExtractMonth


User = get_user_model()

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


