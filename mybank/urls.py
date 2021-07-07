"""Bankproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import UserRegister,LoginView,AccountCreateView,index,Transactionview,signout,ViewBalance,TransactionHistory, \
    RegisterLoginView,UserProfileView,TransactionDebitDetail,TransactionCreditDetail,UserProfileUpdate


urlpatterns = [
    path("register/",UserRegister.as_view(),name="register"),
    path("login/",LoginView.as_view(),name="login"),
    path("accounts/",AccountCreateView.as_view(),name="account"),
    path("index/",index,name="index"),
    path("transactions",Transactionview.as_view(),name="transactions"),
    path("logout",signout,name="signout"),
    path("balEnq",ViewBalance.as_view(),name="balEnq"),
    path("transactionshistory",TransactionHistory.as_view(),name="transactionshistory"),
    path("",RegisterLoginView.as_view(),name="registerlogin"),
    path("userprofile",UserProfileView.as_view(),name="userprofile"),
    path("t_debit/<int:pk>",TransactionDebitDetail.as_view(),name="t_debit"),
    path("t_credit/<int:pk>",TransactionCreditDetail.as_view(),name="t_credit"),
    path("update/<int:pk>",UserProfileUpdate.as_view(),name="update_user_profile")


]
