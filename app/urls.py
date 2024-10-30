from django.urls import path
from .views import (
    home as dasboard_home, 
    main_home, 
    card_list, 
    create_bank_account, 
    confirm_account_activation_payment, 
    confirm_loan_activation_payment,
    confirm_card_payment, 
    card_detail, 
    profile, 
    support_page, 
    register, 
    login_view, 
    create_card, 
    LogoutView, 
    transfer_funds, 
    loans, 
    create_loan,
    loan_detail,
    account_details, 
    accounts_list, 
    transactions, 
    chartpage, validate_transfer, confirm_transfer,
    update_personal_info, update_address_info, update_password, settings,
    welcome_to_check_your_mail

)
urlpatterns = [
    path('', dasboard_home, name="dashboard_home"),
    path('home/', main_home, name="main_home"),
    path('login/', login_view, name="login"),
    path('logout/', LogoutView, name="logout"),
    path('register/', register, name="register"),
    
    path('welcome/', welcome_to_check_your_mail, name="welcome_to_check_your_mail"),


    path('chart/', chartpage, name="chartpage"),

    path('accounts/<int:pk>/', account_details, name="accounts_detail"),
    path('accounts/', accounts_list, name="accounts"),
    path('accounts/create/', create_bank_account, name="create_bank_account"),
    path('confirm-account-payment/<int:pk>/', confirm_account_activation_payment, name="confirm_account_activation_payment"),

    path('transactions/', transactions, name="transactions"),
    path('transfer/', transfer_funds, name="transfer_funds"),


    path('loans/', loans, name="loans"),
    path('create-loan/', create_loan, name="create_loan"),
    path('loan/<int:pk>/', loan_detail, name="loan_detail"),
    path('confirm-loan-activation-payment/<int:pk>/', confirm_loan_activation_payment, name="confirm_loan_activation_payment"),



    path('profile/', profile, name="profile"),
    path('update_personal_info/', update_personal_info, name="update_personal_info"),
    path('update_address_info/', update_address_info, name="update_address_info"),
    path('update_password/', update_password, name="update_password"),



    path('support/', support_page, name="support"),
    path('create-card/', create_card, name="create_card"),
    path('cards/', card_list, name="card_list"),
    path('confirm-card-payment/<int:pk>/', confirm_card_payment, name="confirm_card_payment"),
    path('cards/<int:pk>/', card_detail, name="card_detail"),



    path('validate-transfer/', validate_transfer, name="validate_transfer"),
    path('confirm-transfer/', confirm_transfer, name="confirm_transfer"),



    path('settings/', settings, name="settings"),



]



