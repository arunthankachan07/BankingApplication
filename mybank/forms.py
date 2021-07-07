from django.forms import ModelForm, DateInput
from django import forms

from Bankproject import settings
from .models import CustomUser,Account,Transactions
from bootstrap_datepicker_plus import DatePickerInput



class UserRegistrationForm(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'id': 'pass', 'placeholder': 'Enter Password'}))
    class Meta:
        model=CustomUser
        # fields ="__all__"
        fields = ["username","first_name","last_name","email","password","phone","age" ]
        widgets = {
            'username': forms.TextInput(attrs={'class':'input','id':'user','placeholder':'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'input', 'id': 'user', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'id': 'user', 'placeholder': 'Enter Last Name'}),
            'email': forms.TextInput(attrs={'class': 'input', 'id': 'user', 'placeholder': 'Enter Email Address'}),

            'phone': forms.TextInput(attrs={'class': 'input', 'id': 'user', 'placeholder': 'Enter Your Contact No.'}),
            'age': forms.TextInput(attrs={'class': 'input', 'id': 'user', 'placeholder': 'Enter Your Age'}),


        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'input','id':'user','placeholder':'Enter your username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'input','id':'pass','placeholder':'Enter your password'}))


class CreateAccountForm(ModelForm):
    # user=forms.CharField
    class Meta:
        model=Account

        fields=["account_num","balance","account_type","user","active_status"]
        widgets={
            'account_num':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            'balance':forms.NumberInput(attrs={'class':'form-control'}),
            "account_type":forms.Select(attrs={'class':'form-control'}),
            'user':forms.Select(attrs={'class':'form-control'}),
            'active_status': forms.Select(attrs={'class':'form-control'})

        }

class TransactionCreateForm(forms.Form):
    user=forms.CharField(widget=forms.TextInput(attrs={'class':'text_fields','id':'user','readonly':True}),label="Username")
    to_account_no=forms.CharField(widget=forms.TextInput(attrs={'class':'text_fields','id':'user','placeholder':'Enter Account No'}),label="Account Number")
    confirm_account_no=forms.CharField(widget=forms.TextInput(attrs={'class':'text_fields','id':'user','placeholder':'Confirm Account No '}),label="Confirm Account No")
    amount=forms.CharField(widget=forms.TextInput(attrs={'class':'text_fields','id':'user','placeholder':'Enter Amount'}),label="Amount")
    remarks=forms.CharField(widget=forms.TextInput(attrs={'class':'text_fields','id':'user','placeholder':'Remarks'}),label="Remarks")

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



class UserEditForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email","phone"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),

            'phone': forms.TextInput(attrs={'class': 'form-control'}),


        }

class AccountEditForm(ModelForm):

    class Meta:
        model = Account
        fields = ["account_num","account_type","active_status"]
        widgets = {
            'account_num': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            "account_type": forms.Select(attrs={'class': 'form-control'}),

            'active_status': forms.Select(attrs={'class': 'form-control'})

        }



class HistoryFilterForm(forms.Form):
    #date = forms.DateField(widget=forms.DateInput(attrs={'id':'datepicker','class':'text_inp',}),input_formats=['%d/%m/%Y'],label='Pick Date')
    # date=forms.CharField(widget=forms.TextInput(attrs={'id':'datepicker','class':'text_inp',}),label='Pick Date')
    date = forms.DateField(widget=DateInput(format = '%Y-%m-%d',attrs={'type':'date','class':'form-control-sm'}),label='Pick Date',
                           input_formats=settings.DATE_INPUT_FORMATS)