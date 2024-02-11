
from django.urls import path

from . import views
from .views import (AccountView, AccountView1, EmployeeView, LoanView,
                    PostsView, SiginUpView, UserView, home, index)

urlpatterns = [
    path('index',index),
    path('home',home),
    path('user/', UserView.as_view(), name='user'),
    path('signup/', SiginUpView.as_view(), name='user'),
    path('account/', AccountView.as_view(), name='account'),
    path('employee/', EmployeeView.as_view(), name='account'),
    path('post/<int:pk>', PostsView.as_view(), name='post'),
    path('loan/', LoanView.as_view(), name='loan'),
    path('account1/<int:pk>', AccountView1.as_view(), name='account1'),
    
]
