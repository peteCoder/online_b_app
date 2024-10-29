
from django.urls import path
from .views import create_user, generate_transaction_chart, create_support_request, ConfirmAccountActivationAPIView

urlpatterns = [
    path('users/', create_user, name="create_user"),
    path('charts/', generate_transaction_chart, name="generate_transaction_chart"),

    path('support/', create_support_request, name='create_support_request'),
    path('confirm-account-activation/<int:pk>/', ConfirmAccountActivationAPIView, name='confirm_account_activation'),
]