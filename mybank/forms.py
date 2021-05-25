from django.forms import ModelForm
from django import forms

from .models import CustomUser,Account,Transactions


class UserRegistrationForm(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'id': 'pass', 'placeholder': 'Enter Password'}))
    class Meta:
        model=CustomUser
        # fields ="__all__"
        fields = ["username","email","password","phone","age" ]
        widgets = {
            'username': forms.TextInput(attrs={'class':'input','id':'user','placeholder':'Enter username'}),
            'email': forms.TextInput(attrs={'class': 'input', 'id': 'user', 'placeholder': 'Enter Email Address'}),

            'phone': forms.TextInput(attrs={'class': 'input', 'id': 'user', 'placeholder': 'Enter Your Contact No.'}),
            'age': forms.TextInput(attrs={'class': 'input', 'id': 'user', 'placeholder': 'Enter Your Age'}),


        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'input','id':'user','placeholder':'Enter your username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'input','id':'pass','placeholder':'Enter your password'}))


class CreateAccountForm(ModelForm):
    class Meta:
        model=Account

        fields=["account_num","balance","account_type","user","active_status"]
        widgets={
            'account_num':forms.TextInput(attrs={'readonly':True}),

        }

class TransactionCreateForm(forms.Form):
    user=forms.CharField(widget=forms.TextInput(attrs={'class':'text_inp','id':'user','readonly':True}),label="Username")
    to_account_no=forms.CharField(widget=forms.TextInput(attrs={'class':'text_inp','id':'user','placeholder':'Enter Account No'}),label="Account Number")
    confirm_account_no=forms.CharField(widget=forms.TextInput(attrs={'class':'text_inp','id':'user','placeholder':'Confirm Account No '}),label="Confirm Account No")
    amount=forms.CharField(widget=forms.TextInput(attrs={'class':'text_inp','id':'user','placeholder':'Enter Amount'}),label="Amount")
    remarks=forms.CharField(widget=forms.TextInput(attrs={'class':'text_inp','id':'user','placeholder':'Remarks'}),label="Remarks")

    def clean(self):
        cleaned_data=super().clean()
        to_account_no=cleaned_data.get('to_account_no')
        confirm_account_no=cleaned_data.get('confirm_account_no')
        amount=cleaned_data.get("amount")
        user=cleaned_data.get("user")
        try:
            account=Account.objects.get(account_num=to_account_no)
        except:
            msg = "Invalid account number"
            self.add_error('to_account_no', msg)
        if to_account_no != confirm_account_no:
            msg="account number mismatch"
            self.add_error('to_account_no',msg)

        account=Account.objects.get(user__username=user)
        avlbalance=account.balance
        if int(amount)>int(avlbalance):
            message="insufficient balance"
            self.add_error('amount',message)