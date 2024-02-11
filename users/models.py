from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, mobile,  password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, mobile,  password, **other_fields)

    def create_user(self, email, mobile,  password, **other_fields):

        if not mobile:
            raise ValueError(_('You must provide an mobile number'))
        user = self.model(email=email, mobile=mobile,
                           **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser,PermissionsMixin):
    class Meta:
        db_table = 'user'
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=15)
    # username = models.CharField(max_length=12)
    mobile = models.CharField(max_length=10,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomAccountManager()
    USERNAME_FIELD='mobile'
    REQUIRED_FIELDS = [ 'name','email']

class Account(models.Model):
    accountType_choice=(("Savings","Savings"),
                    ("Current","Current"))
    class Meta:
        db_table = 'account'
    accountType = models.CharField(max_length=30,choices=accountType_choice,default="Savings")
    amount = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Loan(models.Model):
    class Meta:
        db_table = 'loan'
    amount = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Employee(models.Model):
    class Meta:
        db_table = 'employee'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    salary = models.IntegerField()
    apointedDate = models.DateTimeField()
    

class Posts(models.Model):
    class Meta:
        db_table = 'post'

    # id = models.IntegerField()
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)