from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from mybank.models import CustomUser,Transactions,Account

class AccountModelSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ["account_num", "balance", "account_type", "user", "active_status"]


class UserModelSerializer(ModelSerializer):
    class Meta:
        model= CustomUser
        fields = ["username", "first_name", "last_name", "email", "password", "phone", "age"]

class TransactionModelSerializer(ModelSerializer):
    class Meta:
        model=Transactions
        fields="__all__"
