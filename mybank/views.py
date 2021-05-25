from django.contrib.auth import authenticate,login as djangologin,logout
from django.http import JsonResponse
from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView
from .forms import UserRegistrationForm,LoginForm,CreateAccountForm,TransactionCreateForm
from .models import CustomUser,Account,Transactions
from django.utils.decorators import method_decorator
from .decorators import account_created_validator,login_required
from django.http import HttpResponse

class UserRegister(TemplateView):
    model=CustomUser
    template_name = "mybank/register.html"
    context={}
    form_class=UserRegistrationForm
    def get(self, request, *args, **kwargs):
        self.context["form"]=self.form_class
        return render(request,self.template_name,self.context)
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():

            form.save()
            print("saved")
            return redirect("login")
        else:

            self.context["form"]=form
            return render(request,self.template_name,self.context)

class LoginView(TemplateView):
    model=CustomUser
    template_name = "mybank/login.html"
    form_class=LoginForm
    context={}
    def get(self, request, *args, **kwargs):
        self.context["form"]=self.form_class()
        return render(request,self.template_name,self.context)
    def post(self,request, *args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            # user=authenticate(request,username=username,password=password)
            user=self.model.objects.get(username=username)
            if (user.username==username)&(user.password==password):
                djangologin(request,user)
                print("success")
                return redirect("index")
            else:
                print("failed")
                self.context["form"]=self.form_class()
                return render(request, self.template_name, self.context)
        else:
            print("failed")
            self.context["form"] = form
            return render(request, self.template_name, self.context)


#Registration and login in same template
class RegisterLoginView(TemplateView):
    model=CustomUser
    template_name = "mybank/register_login.html"
    sign_in_form=LoginForm
    sign_up_form=UserRegistrationForm
    context={}
    def get(self, request, *args, **kwargs):
        print("test")
        self.context["form"]={'sign_in_form':self.sign_in_form,'sign_up_form':self.sign_up_form}
        return render(request,self.template_name,self.context)
    def post(self, request, *args, **kwargs):
        #----------login codes-------------
        if "signin" in request.POST:
            print("signin")
            form = self.sign_in_form(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                # user=authenticate(request,username=username,password=password)
                user = self.model.objects.get(username=username)
                if (user.username == username) & (user.password == password):
                    djangologin(request, user)
                    print("success")
                    return redirect("index")

                else:
                    print("failed")
                    self.context["form"] = {'sign_in_form': self.sign_in_form, 'sign_up_form': self.sign_up_form}
                    return render(request, self.template_name, self.context)
            else:
                self.context["form"] = {'sign_in_form': self.sign_in_form, 'sign_up_form': self.sign_up_form}
                return render(request, self.template_name, self.context)

        #---------registration code----------
        elif "signup" in request.POST:
            print("signup")
            form = self.sign_up_form(request.POST)
            if form.is_valid():

                form.save()
                print("saved")
                return redirect("registerlogin")
            else:

                self.context["form"] = form
                return render(request, self.template_name, self.context)
        else:
            self.context["form"] = {'sign_in_form': self.sign_in_form, 'sign_up_form': self.sign_up_form}
            return render(request, self.template_name, self.context)


@method_decorator(login_required,name='dispatch')
@method_decorator(account_created_validator,name='dispatch')
class AccountCreateView(TemplateView):
    model=Account
    template_name = "mybank/createaccount.html"
    form_class=CreateAccountForm
    context={}
    def get(self, request, *args, **kwargs):
        account_num=""
        account=self.model.objects.all().last()
        if account:
           accno=int(account.account_num.split("-")[1])+1
           account_num="SBK-"+str(accno)
        else:
            account_num="SBK-1000"
        self.context["form"]=self.form_class(initial={"account_num":account_num,"user":request.user})
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            self.context["form"]=form
            return render(request,self.template_name,self.context)

@login_required
def index(request):
    context={}
    try:
        account = Account.objects.get(user=request.user)
        status = account.active_status
        flag = True if status == "Active" else False
        context["flag"] = flag
        return render(request, "mybank/home.html", context)
    except:
        return render(request, "mybank/home.html", context)


class GetUser(object):
    def get_user(self,account_num):
        return Account.objects.get(account_num=account_num)

@method_decorator(login_required,name='dispatch')

class Transactionview(TemplateView,GetUser):
    model= Transactions
    template_name = "mybank/transactions.html"
    form_class=TransactionCreateForm
    context={}
    def get(self, request, *args, **kwargs):
        try:
            current_acc = Account.objects.get(user=request.user)
            status=current_acc.active_status
            print(status)
            if status =="Inactive":
                msg = "Sorry,Your Account is not Activated!"
                return render(request, self.template_name, {'msg': msg})
            else:
                self.context["form"]=self.form_class(initial={'user':request.user})
                return render(request,self.template_name,self.context)
        except:
            message = "Sorry,You have no Account Created!"
            return render(request,self.template_name, {'message': message})
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():

            to_account=form.cleaned_data.get('to_account_no')
            amount=form.cleaned_data.get('amount')
            remarks=form.cleaned_data.get('remarks')
            account=self.get_user(to_account)
            account.balance+=int(amount)
            account.save()
            current_acc=Account.objects.get(user=request.user)
            current_acc.balance-=int(amount)
            current_acc.save()
            transaction=Transactions(user=request.user,
                                     amount=amount,
                                     to_accno=to_account,
                                     remarks=remarks)
            transaction.save()

            return redirect("index")
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)

@method_decorator(login_required,name='dispatch')
class ViewBalance(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            account=Account.objects.get(user=request.user)
            balance=account.balance
            print(balance)
            return JsonResponse({'balance':balance})
        except:
            balance=0;
            print(balance)
            return JsonResponse({'balance': balance})

@method_decorator(login_required,name='dispatch')
class TransactionHistory(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            debit_transactions = Transactions.objects.filter(user=request.user)
            l_user = Account.objects.get(user=request.user)
            credit_transactions = Transactions.objects.filter(to_accno=l_user.account_num)
            return render(request, "mybank/transactionshistory.html", {'dtransactions': debit_transactions,
                                                                       'ctransactions': credit_transactions})
        except:

            message="You have no Account Created!"
            return render(request, "mybank/transactionshistory.html", {'message':message})


def signout(request):
    logout(request)
    return redirect("registerlogin")