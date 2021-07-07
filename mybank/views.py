from django.contrib.auth import authenticate,login as djangologin,logout
from django.http import JsonResponse
from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView
from .forms import UserRegistrationForm,LoginForm,CreateAccountForm,TransactionCreateForm,UserEditForm,AccountEditForm,HistoryFilterForm
from .models import CustomUser,Account,Transactions
from django.utils.decorators import method_decorator
from .decorators import account_created_validator,login_required
from django.http import HttpResponse
from django.contrib import messages
from django.forms.models import model_to_dict

from twilio.rest import Client
from django.conf import settings

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
                try:
                    user = self.model.objects.get(username=username)
                    if user.username == username:
                        if user.password == password:
                            djangologin(request, user)
                            print("success")
                            return redirect("index")
                        else:
                            messages.error(request, 'Password is incorrect')
                            self.context["form"] = {'sign_in_form': self.sign_in_form,
                                                    'sign_up_form': self.sign_up_form}
                            return render(request, self.template_name, self.context)
                    else:
                        messages.error(request, 'Username or password incorrect')
                        self.context["form"] = {'sign_in_form': self.sign_in_form,
                                                'sign_up_form': self.sign_up_form}
                        return render(request, self.template_name, self.context)
                except:
                    messages.error(request, 'Invalid Username or password')
                    self.context["form"] = {'sign_in_form': self.sign_in_form, 'sign_up_form': self.sign_up_form}
                    return render(request, self.template_name, self.context)
            else:
                messages.error(request, 'Invalid Username or password')
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
        # status = account.active_status
        # flag = True if status == "Active" else False
        flag = True if account else False
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
            flag = True if current_acc else False

            status=current_acc.active_status
            print(status)
            if status =="Inactive":
                msg = "Sorry,Your Account is not Activated!"
                return render(request, self.template_name, {'msg': msg,'flag':flag})
            else:
                form=self.form_class(initial={'user':request.user})
                return render(request,self.template_name,{'form':form,'flag':flag})
        except:
            msg1 = "Sorry,You have no Account Created!"
            return render(request,self.template_name, {'msg1': msg1})
    def post(self,request,*args,**kwargs):
        current_acc = Account.objects.get(user=request.user)
        flag = True if current_acc else False
        form = self.form_class(request.POST)
        if form.is_valid():

            to_account=form.cleaned_data.get('to_account_no')
            amount=form.cleaned_data.get('amount')
            remarks=form.cleaned_data.get('remarks')
            account=self.get_user(to_account)
            if account.active_status=="Active":
                trans=True
                print(account.active_status)
                account.balance+=int(amount)
                account.save()
                current_acc=Account.objects.get(user=request.user)
                current_acc.balance-=int(amount)
                current_acc.save()
                fromaccno=current_acc.account_num
                transaction=Transactions(user=request.user,
                                         amount=amount,
                                         to_accno=to_account,
                                         remarks=remarks,
                                         from_accno=fromaccno)

                transaction.save()

                messages.success(request, 'Transaction Successful')
                acc=Account.objects.get(account_num=to_account)
                user_det=CustomUser.objects.get(username=acc.user)
                t_det = Transactions.objects.all().last()
                # Twilio Sms Sending
                # to = '+91'+user_det.phone
                # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                # response = client.messages.create(
                #     body='Dear Customer, Rs.'+str(amount)+'credited to your A/c'+to_account+'from A/c'+fromaccno+
                #          '.Available Bal- Rs.'+str(acc.balance)+'-SBK BANK',
                #     to=to, from_=settings.TWILIO_PHONE_NUMBER)
                # --------------


                return render(request, self.template_name,{'acc':acc,'user_det':user_det,'trans':trans,'flag':flag,'t_det':t_det})
            else:
                messages.error(request, 'Transaction Failed')


                return render(request, self.template_name,{'flag':flag})


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
    model = Transactions
    template_name = "mybank/transactionshistory.html"
    form_class = HistoryFilterForm
    context = {}
    def get(self, request, *args, **kwargs):
        try:
            form = self.form_class
            debit_transactions = Transactions.objects.filter(user=request.user).order_by('-id')[:5]
            l_user = Account.objects.get(user=request.user)
            flag = True if l_user else False
            credit_transactions = Transactions.objects.filter(to_accno=l_user.account_num).order_by('-id')[:5]
            return render(request, "mybank/transactionshistory.html", {'dtransactions': debit_transactions,
                                                                       'ctransactions': credit_transactions,'flag':flag,'form':form})
        except:
            message="You have no Account Created!"
            return render(request, "mybank/transactionshistory.html", {'message':message})
    def post(self, request, *args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            date=form.cleaned_data.get('date')
            print(date)
            debit_transactions = Transactions.objects.filter(user=request.user)
            on_date_debit=debit_transactions.filter(date=date)
            l_user = Account.objects.get(user=request.user)
            flag = True if l_user else False
            credit_transactions = Transactions.objects.filter(to_accno=l_user.account_num)
            on_date_credit=credit_transactions.filter(date=date)
            return render(request, "mybank/transactionshistory.html", {'dtransactions': on_date_debit,
                                                                       'ctransactions': on_date_credit,
                                                                       'flag': flag, 'form': form})


@method_decorator(login_required,name='dispatch')
class TransactionDebitDetail(TemplateView):
    def get(self, request, *args, **kwargs,):
        id=kwargs.get("pk")
        debit_transactions = Transactions.objects.get(id=id)
        # data={'id':debit_transactions.id,'amount':debit_transactions.amount,'to_accno':debit_transactions.to_accno}
        # data=serializers.serialize('json',debit_transactions)
        print(model_to_dict(debit_transactions))
        return JsonResponse(model_to_dict(debit_transactions))

@method_decorator(login_required,name='dispatch')
class TransactionCreditDetail(TemplateView):
    def get(self, request, *args, **kwargs,):
        id=kwargs.get("pk")
        credit_transactions = Transactions.objects.get(id=id)
        print(credit_transactions.date)
        return JsonResponse(model_to_dict(credit_transactions))

def signout(request):
    logout(request)
    return redirect("registerlogin")

class UserProfileView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            user=CustomUser.objects.get(username=request.user)
            account=Account.objects.get(user=request.user)
            flag = True if account else False

            return render(request,"mybank/userprofile.html",{'user':user, 'account':account,'flag':flag})
        except:
            user = CustomUser.objects.get(username=request.user)
            return render(request, "mybank/userprofile.html", {'user': user})


class UserProfileUpdate(TemplateView):
    user_model = CustomUser
    account_model=Account
    template_name = "mybank/updateprofile.html"
    user_form = UserEditForm
    account_form= AccountEditForm
    context = {}
    lookup=0
    def get(self, request, *args, **kwargs):
        self.lookup=kwargs.get("pk")
        try:
            user=self.user_model.objects.get(id=self.lookup)
            account=self.account_model.objects.get(user_id=user.id)
            form_user=self.user_form(instance=user)
            form_account=self.account_form(instance=account)
            return render(request, self.template_name, {'form_user': form_user,'form_account': form_account})
        except:
            user = self.user_model.objects.get(id=self.lookup)
            form_user = self.user_form(instance=user)
            return render(request, self.template_name, {'form_user': form_user})
    def post(self,request,*args,**kwargs):
        self.lookup = kwargs.get("pk")
        try:
            user = self.user_model.objects.get(id=self.lookup)
            account = self.account_model.objects.get(user_id=user.id)
            form_user = self.user_form(request.POST, instance=user)
            form_account = self.account_form(request.POST, instance=account)
            print("test")
            if (form_user.is_valid()) & (form_account.is_valid()):
                form_user.save()
                form_account.save()
                print("success1")
                return redirect("userprofile")
            else:
                print("failed")
                return render(request, self.template_name, {'form_user': form_user, 'form_account': form_account})
        except:
            user = self.user_model.objects.get(id=self.lookup)
            form_user = self.user_form(request.POST, instance=user)
            print("test")
            if form_user.is_valid():
                form_user.save()
                print("success1")
                return redirect("userprofile")
            else:
                print("failed")
                return render(request, self.template_name, {'form_user': form_user})

