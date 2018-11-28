# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
# Create your models here.

class IMG(models.Model):
    img = models.ImageField(upload_to='img')  #指定上传的图片存储的文件夹
    name = models.CharField(max_length=20)
    # user = models.ForeignKey(User, default='1')


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','email')

admin.site.register(User, UserAdmin)