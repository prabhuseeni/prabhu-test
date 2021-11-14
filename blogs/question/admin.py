from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email')
admin.site.register(MyUser, MyUserAdmin)