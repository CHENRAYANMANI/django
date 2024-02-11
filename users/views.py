
from datetime import datetime

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
# from rest_framework import generics
from rest_framework.views import APIView

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

from .models import Account, Employee, Loan, Posts, User


# Create your views here.
def index(request):
    return HttpResponse('hello world')

def home(request):
    return render(request,'home.html',{'name1':'chenrayan'})


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # print('request.user',request.user.name)
        data = User.objects.get(id=request.user.id)
        return Response(model_to_dict(data),status=status.HTTP_200_OK) 

   
class SiginUpView(APIView):
     def post(self,request):
        data = request.data
        try:
            instance = User.objects.create(name=data["name"],email=data["email"],mobile = data["mobile"])
            if data["password"] is not None:
                instance.set_password(data["password"])
            instance.save()
            return Response({'ok':200},status=status.HTTP_200_OK)  
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)

class AccountView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        data = Account.objects.filter(user=request.user).values("amount","accountType","user__name","user__email","user__mobile")
        print('data',data)
        return Response(data,status=status.HTTP_200_OK) 
    
    
    def post(self,request):
        data = request.data
        data['user']=request.user
        # user_instance = User.objects.get(id=int(data["user"]))
        # instance = Account.objects.create(accountType=data["accountType"],amount=data["amount"],user = request.user)
        instance = Account(**data)
        instance.save()
        return Response({'ok':200},status=status.HTTP_200_OK)  
    
class LoanView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = Loan.objects.filter(user=request.user).values("amount","user__name","user__email","user__mobile")
        # print('data',data)
        return Response(data,status=status.HTTP_200_OK) 
    
    
    def post(self,request):
        
        data = request.data
        # user_instance = User.objects.get(id=int(data["user"]))
    
        instance = Loan.objects.create(amount=data["amount"],user = request.user)
        instance.save()
        return Response({'ok':200},status=status.HTTP_200_OK)  

class EmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        # data = Employee.objects.filter(user=request.user).values('first_name','last_name','salary','apointedDate') 
        data = Employee.objects.all().values('first_name','last_name','salary','apointedDate') 
        return Response(data,status=status.HTTP_200_OK)
    
    def post(self,request):
        data = request.data
        instance = Employee.objects.create(first_name=data['first_name'],last_name=data['last_name'],salary=data['salary'],apointedDate=data['apointedDate'])
        instance.save()
        return Response({'ok':200},status=status.HTTP_200_OK) 


class PostsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,pk):
        # data = Employee.objects.filter(user=request.user).values('first_name','last_name','salary','apointedDate') 
        data = Posts.objects.filter(user=request.user).values('id','title','date','body') 
        return Response(data,status=status.HTTP_200_OK)
    
    def post(self,request,pk):
        data = request.data
        instance = Posts.objects.create(title=data['title'],date=datetime.now(),body=data['body'],user=request.user)
        instance.save()

        return Response(model_to_dict(instance),status=status.HTTP_200_OK) 
    
    def delete(self, request, pk):
        post = Posts.objects.get(id=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self,request,pk):
        post = Posts.objects.get(pk=pk)
        data = request.data
        post.title=data['title']
        post.body=data['body']
        post.save()
        return Response(model_to_dict(post),status=status.HTTP_200_OK) 


# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


class AccountView1(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request,pk):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request,pk):
        request.data['user']=request.user.id
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        account = Account.objects.get(pk=pk)
        request.data['user']=request.user.id
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        request.data['user']=request.user.id
        account = Account.objects.get(pk=pk)
        serializer = AccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = Account.objects.get(pk=pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@receiver(pre_save, sender=Account)
def my_model_pre_save(sender, instance, **kwargs):
    print('Account pre save',instance)
    """
    This function will be called before saving a MyModel instance.
    """
    # Perform some action before saving the MyModel instance
    # For example, modify the instance attributes or perform additional checks
    pass
