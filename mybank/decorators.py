from django.contrib import messages
from django.shortcuts import redirect

from mybank.models import Account


def account_created_validator(func):
    def wrapper(request,*args,**kwargs):
        try:
            account = Account.objects.get(user=request.user)
            status = account.active_status
            if (status == "Active") & (status=="Inactive"):
            # if account:
                messages.error(request,"account created for this user")
                return redirect("index")
            else:
                return func(request,*args,**kwargs)
        except:
            return func(request, *args, **kwargs)
    return wrapper

def login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            return redirect("registerlogin")
    return wrapper

