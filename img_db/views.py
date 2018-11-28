# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
django.setup()

from django.shortcuts import render, redirect
from img_db.models import IMG
import cv2

from django import forms
from models import User

# Create your views here.
def uploadImg(request):
    if request.method == 'POST':
        label2 = 0 #用于文件类型判断的标志
        img_map = ['.jpg', '.png']

        image = request.FILES.get('image')

        if image == None:
            return render(request, 'img_tem/uploadimg.html', {'result': '请上传参赛图片!'})

        for i in range(0, len(img_map)):
            if image.name.endswith(img_map[i]):
                label2 = 1

        if label2 == 0:
            return render(request, 'img_tem/uploadimg.html', {'result': '上传失败，请上传.jpg或者.png的图片！'})
        else:
            # 这里先把文件保存成临时的文件temp.png
            f = open('temp.png', 'wb')
            f.write(image.read())
            f.close()
            # 然后opencv通过temp.png这个文件名去读取文件
            # 这个时候图片还没有保存到数据库里
            image_cv = cv2.imread('temp.png')
            gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.15,
                minNeighbors=5,
                minSize=(5, 5),
            )
            face_num = len(faces)
            if face_num == 1:
                if '_' in image.name:
                    new_img = IMG(
                    img=image,
                    name=image.name.replace(img_map[i], ''),
                    # user=request.user
                    )
                    new_img.save()
                    return render(request, 'img_tem/uploadimg.html', {'result': '上传成功！'})
                else:
                    return render(request, 'img_tem/uploadimg.html', {'result': '上传失败，图片名称格式不对，请以“学校_姓名”命名！'})
            elif face_num > 1:
                return render(request, 'img_tem/uploadimg.html', {'result': '上传失败，此图片为多人合照，请上传本人照片！'})
            else:
                return render(request, 'img_tem/uploadimg.html', {'result': '上传失败，此图片为风景照，请上传本人照片！'})
    return render(request, 'img_tem/uploadimg.html')


def showImg(request):
    imgs = IMG.objects.all()
    for i in imgs:
        print(i.img.url)           #把图片的地址打印一下
    return render(request, 'img_tem/showimg.html', {'imgs': imgs})

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')

def regist(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            filter_result = User.objects.filter(username=username)
            if len(filter_result)>0:
                return render(request, 'regist_failure.html', {'result':'用户名已经存在,请重新注册！'})
            else:
                password = userform.cleaned_data['password']
                email = userform.cleaned_data['email']

                user = User.objects.create(username=username,password=password,email=email)
                user.save()

                return render(request, 'regist_success.html')
    else:
        userform = UserForm()
    return render(request, 'regist.html', {'userform':userform})

def login(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']

            user = User.objects.filter(username=username,password=password)

            if user:
                return redirect('/upload/')
            else:
                return render(request, 'login_failure.html')

    else:
        userform = UserForm()
    return render(request, 'login.html', {'userform': userform})

def index(request):
    return render(request, 'index.html')

