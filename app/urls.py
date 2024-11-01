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
    connect_card,
    transactions, 
    chartpage, validate_transfer, confirm_transfer,
    update_personal_info, update_address_info, update_password, settings,
    welcome_to_check_your_mail, about_page, cancer_page

)
urlpatterns = [
    
    path('', main_home, name="main_home"),
    path('about/', about_page, name="about_page"),
    path('cancer/', cancer_page, name="cancer_page"),






    path('login/', login_view, name="login"),
    path('logout/', LogoutView, name="logout"),
    path('register/', register, name="register"),
    
    path('welcome/', welcome_to_check_your_mail, name="welcome_to_check_your_mail"),


    path('chart/', chartpage, name="chartpage"),

    path('dashboard/', dasboard_home, name="dashboard_home"),
    path('dashboard/accounts/<int:pk>/', account_details, name="accounts_detail"),
    path('dashboard/accounts/', accounts_list, name="accounts"),
    path('dashboard/accounts/create/', create_bank_account, name="create_bank_account"),
    path('dashboard/confirm-account-payment/<int:pk>/', confirm_account_activation_payment, name="confirm_account_activation_payment"),

    path('dashboard/transactions/', transactions, name="transactions"),
    path('dashboard/transfer/', transfer_funds, name="transfer_funds"),


    path('dashboard/loans/', loans, name="loans"),
    path('dashboard/create-loan/', create_loan, name="create_loan"),
    path('dashboard/loan/<int:pk>/', loan_detail, name="loan_detail"),
    path('dashboard/confirm-loan-activation-payment/<int:pk>/', confirm_loan_activation_payment, name="confirm_loan_activation_payment"),



    path('dashboard/profile/', profile, name="profile"),
    path('dashboard/update_personal_info/', update_personal_info, name="update_personal_info"),
    path('dashboard/update_address_info/', update_address_info, name="update_address_info"),
    path('dashboard/update_password/', update_password, name="update_password"),



    path('dashboard/support/', support_page, name="support"),
    path('dashboard/create-card/', create_card, name="create_card"),
    path('dashboard/connect-card/', connect_card, name="connect_card"),
    path('dashboard/cards/', card_list, name="card_list"),
    path('dashboard/confirm-card-payment/<int:pk>/', confirm_card_payment, name="confirm_card_payment"),
    path('dashboard/cards/<int:pk>/', card_detail, name="card_detail"),



    path('dashboard/validate-transfer/', validate_transfer, name="validate_transfer"),
    path('dashboard/confirm-transfer/', confirm_transfer, name="confirm_transfer"),



    path('dashboard/settings/', settings, name="settings"),



]



