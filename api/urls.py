
from django.urls import path
from .views import create_user, generate_transaction_chart

urlpatterns = [
    path('users/', create_user, name="create_user"),
    path('charts/', generate_transaction_chart, name="generate_transaction_chart"),
]