import json
import os
import time

from django.contrib import auth
from django.contrib.auth import logout
from django.core import serializers
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators import gzip

from Web_End import settings
from veision1 import models, video
from veision1.models import User


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        # return render(request,"index.html")
        # 前端 变量名称为email_username
        email_username = request.POST['email']
        if(not '@' in email_username):
            information = {"information":"User name is incorrectly formatted"}
            return render(request, "login.html", information)
        # 前端 变量名称为pw
        password = request.POST['password']

        hasUser =  User.objects.filter(email=email_username)
        if len(password) < 6:
            information = {"information": "Password is not less than six digits"}
            return render(request, "login.html", information)
        if hasUser:
            user = auth.authenticate(email=email_username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/version1/add_information")
            else:
                information = {"information":"Wrong user name or password"}
                return render(request,"login.html",information)
        else:
            information = {"information":"User name does not exist"}
            return render(request, "login.html", information)
    return render(request, 'login.html')

def index(request):
    # label = {}
    # label["page2"]="current_page"
    # label["title"]="情感检测"
    # data = render_to_string("cv_template.html")
    # label["data"] = data
    return render(request,"video_player.html")

def add_information(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # 拿到提交的表单
            form = {}
            for element in request.POST:
                if element == "csrfmiddlewaretoken":
                    continue
                form[element] = request.POST[element]

            photo = request.FILES.get('photo')
            photoname = request.user.email + photo.name
            path = os.path.join(settings.MEDIA_ROOT, 'user_photo', photoname)
            with open(path, 'wb') as pic:
                for p in photo.chunks():
                    pic.write(p)
            form["photo"] = photoname
            form["user_email"] = request.user.email

            s = models.ManageInfo.objects.create(**form)
            s.save()

            return redirect("/version1/get_information")
        label = {}
        label["page7"] = "current_page"
        label["title"] = "添加个人信息"
        return render(request,"information_add.html",label)
    return redirect("/version1/login")

def get_information(request):
    if request.user.is_authenticated:
        email = request.user.email
        manager = models.ManageInfo.objects.filter(user_email=email)
        if manager:
            email = request.user.email
            manager = models.ManageInfo.objects.filter(user_email = email)
            user_data = json.loads(serializers.serialize("json", manager))
            content = user_data[0]["fields"]
            content["page7"] = "current_page"
            content["title"] = "个人信息"
            return render(request,"information_get.html",content)
        else:
            return redirect("/version1/add_information")
    return redirect("/version1/login")

def fix_information(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            # 拿到提交的表单
            email = request.user.email
            manager = models.ManageInfo.objects.filter(user_email=email)
            user_data = json.loads(serializers.serialize("json", manager))
            content = user_data[0]["fields"]

            form = {}
            for element in request.POST:
                if element == "csrfmiddlewaretoken":
                    continue
                form[element] = request.POST[element]

            photo = request.FILES.get('photo')
            form["photo"] = content["photo"]
            if photo is not None:
                photoname = request.user.email + photo.name
                form["photo"] = photoname
                path = os.path.join(settings.MEDIA_ROOT, 'user_photo', photoname)
                with open(path, 'wb') as pic:
                    for p in photo.chunks():
                        pic.write(p)
            form["user_email"] = request.user.email

            manager.delete()
            s = models.ManageInfo.objects.create(**form)
            s.save()

            return redirect("/version1/get_information")
        email = request.user.email
        manager = models.ManageInfo.objects.filter(user_email = email)
        user_data = json.loads(serializers.serialize("json", manager))
        content = user_data[0]["fields"]
        content["page7"] = "current_page"
        content["title"] = "修改个人信息"
        return render(request,"information_fix.html",content)
    return redirect("/version1/login")

def emotion_detection(request):
    label = {}
    label["page2"] = "current_page"
    label["title"] = "情感检测"
    label["say"] = "情感检测的数据显示界面"
    return render(request, "video_player.html", label)

def just_for_test(request):
    return render(request, "just_for_test.html")

def gen():
    while True:
        time.sleep(1)
        frame = str(time.time()).encode("utf-8")
        yield (b'--frame\r\n'
               b'Content-Type: text/plain;charset=utf-8\r\n\r\n' + frame + b'\r\n\r\n')

def list_data(request):
    return StreamingHttpResponse(gen(), content_type="multipart/x-mixed-replace; boundary=frame")




def logout1(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/version1/login")

def create_user1(request):
    a = models.User.objects.create_user(email="1234@qq.com", password="111111")
    a.save()
    return redirect("/login")

def video_page(request):
    return render(request,"just_for_test.html")

@gzip.gzip_page
def get_video(request):
    return StreamingHttpResponse(video.generetor(),content_type='multipart/x-mixed-replace;boundary=frame')

def websocket_page(request):
    return render(request,"just_for_test.html")

def get_face(request):
    return render(request,"get_face.html")

def post_photo(request):
    return HttpResponse("OK")






