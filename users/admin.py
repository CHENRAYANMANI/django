from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account, Employee, Loan, Posts, User


# Register your models here.
class UserConfigAdmin(UserAdmin):
    model = User
    list_display = ('mobile','name','email',)
    ordering = ('-id',)
    fieldsets = (
        (None, {'fields': ('mobile','email',  'name','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}))
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile','email',  'name','password', 'is_active', 'is_staff','is_superuser')}
         ),
    )
    # list_filter = ('recommended_by', )
admin.site.register(User, UserConfigAdmin)

@admin.register(Account)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id","accountType","amount")
    # list_filter = ('recommended_by_id','lastlogin_date','available_margin' )

@admin.register(Loan)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id","amount")


@admin.register(Employee)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Employee._meta.get_fields()]

@admin.register(Posts)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Posts._meta.get_fields()]