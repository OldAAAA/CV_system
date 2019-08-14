import json

from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from veision1 import models
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from Web_End import settings
import os

host1 = "192.168.43.18:8000"
# host1 = "192.168.43.18:8000"
# host2 = "192.168.1.103:8000"
host2 = "192.168.43.36:8000"


def emotion_detection(request):
    label = {}
    label["page2"] = "current_page"
    label["title"] = "情感检测"
    label["bigtitle"] = "情感检测"
    label["smalltitle"] = "持续关注老人心理健康"
    label["say"] = "情感检测信息实时显示"
    label["roonname"] = "emotion"
    # label["ipport"] = "192.168.1.108:8000"
    # label["ipport"] = "192.168.1.102:8000/version1"
    label["ipport"] = host1
    label["num"] = "1"

    return render(request, "video_player.html", label)

def stranger_detection(request):
    label = {}
    label["page3"] = "current_page"
    label["title"] = "陌生人检测"
    label["bigtitle"] = "陌生人检测"
    label["smalltitle"] = "营造安全的养老环境"
    label["say"] = "陌生人检测数据显示界面"
    label["roonname"] = "stranger"
    # label["ipport"] = "192.168.1.108:8000"
    # label["ipport"] = "127.0.0.1:8000/version1"
    label["ipport"] = host1
    label["num"] = "2"
    label["music"] = "dangerous_unknown"
    return render(request, "video_player.html", label)

def volunteer_interaction_detection(request):
    label = {}
    label["page4"] = "current_page"
    label["title"] = "义工交互检测"
    label["bigtitle"] = "义工交互检测"
    label["smalltitle"] = "实时显示老人与义工的交互情况"
    label["say"] = "义工交互检测数据显示界面"
    label["roonname"] = "interact"
    label["ipport"] = host1
    label["num"] = "3"
    return render(request, "video_player.html", label)

def fall_detection(request):
    label = {}
    label["page5"] = "current_page"
    label["title"] = "摔倒检测"
    label["bigtitle"] = "摔倒检测"
    label["smalltitle"] = "第一时间检测老人摔倒"
    label["ipport"] = host2
    label["num"] = "2"
    label["say"] = "摔倒检测的数据显示界面"
    label["roonname"] = "fall"
    label["music"] = "dangerous_fall"
    return render(request, "video_player.html", label)

def intrusion_detection(request):
    label = {}
    label["page6"] = "current_page"
    label["title"] = "入侵检测"
    label["say"] = "入侵检测的数据显示界面"
    label["bigtitle"] = "入侵检测"
    label["smalltitle"] = "让老人远离危险"
    label["roonname"] = "attack"
    label["ipport"] = host2
    label["num"] = "3"
    label["music"] = "dangerous_attack"
    return render(request, "video_player.html", label)

#搜索查看老人信息
@csrf_exempt
def elderly_information_management(request):
    label = {}
    label["page1"] = "current_page"
    label["title"] = "老人信息管理"

    elderlyList = []
    cursor = connection.cursor();

    print(request.method)

    if request.method == "POST":
        print("搜索")
        if request.POST.get('if_search')=="search":
            search_info = request.POST.get('elderly_search_info')
            if search_info:
                elderlyList += dictfetchall(cursor.execute('select * from veision1_elderlyinfo where name LIKE \'%{}%\''.format(search_info)))
                elderlyList += dictfetchall(cursor.execute('select * from veision1_elderlyinfo where id_card LIKE \'%{}%\''.format(search_info)))
                print("搜索")
                print(elderlyList)
            else:
                elderlyList += dictfetchall(cursor.execute('select * from veision1_elderlyinfo'))
                print("搜索")
                print(elderlyList)
            data = render_to_string("elderly_information.html", {'elderlyList': elderlyList,'search_info':search_info})
            label["data"] = data
            return render(request, "index.html", label )

    cursor.execute('select * from veision1_elderlyinfo')
    elderlyList += dictfetchall(cursor);
    print("老人")
    print(elderlyList)

    data = render_to_string("elderly_information.html",{'elderlyList': elderlyList})
    label["data"] = data
    return render(request, "index.html", label,)

#添加老人
@csrf_exempt
def add_elderly(request):
    if request.method== "POST":
        print("增加老人")
        # 拿到提交的表单
        form = {}
        for element in request.POST:
            if element == "csrfmiddlewaretoken":
                continue
            form[element] = request.POST[element]

        photo = request.FILES.get('photo')
        print("")
        print(photo)
        path = os.path.join(settings.MEDIA_ROOT, 'elderly',photo.name)
        with open(path, 'wb') as pic:
            for p in photo.chunks():
                pic.write(p)
        form["photo"] = "../static/media/elderly/" + photo.name

        s = models.elderlyInfo.objects.create(**form)
        s.save()

        label = {}
        label["page1"] = "current_page"
        label["title"] = "老人信息管理"
        elderlyList = []
        cursor = connection.cursor();
        cursor.execute('select * from veision1_elderlyinfo')
        elderlyList += dictfetchall(cursor);
        data = render_to_string("elderly_information.html", {'elderlyList': elderlyList})
        label["data"] = data
        return render(request, "index.html", label, )
    return render(request, "add_elderly.html")

# 删除老人
def delete_elderly(request):
    if request.method == 'GET':
        print("执行删除")
        id = request.GET['elderly_id']
        print(id)
        cursor = connection.cursor();
        cursor.execute('delete from veision1_elderlyinfo where id = \'{}\''.format(id))
        res = {}
        res['cool'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')

# 修改老人信息
def modify_elderly(request):
    if request.method == "POST":
        cursor = connection.cursor()
        id = request.POST.get('id')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        phone_number = request.POST.get('phone_number')
        id_card = request.POST.get('id_card')
        age = request.POST.get('age')
        photo = request.FILES.get('photo')
        one = models.elderlyInfo.objects.get(id=id)
        if one:
            one.name = name
            one.sex = sex
            one.phone_number = phone_number
            one.id_card = id_card
            one.age = age
            if photo:
                photo_path = "../static/media/elderly/"+photo.name
                print("photopath")
                print(photo_path)
                one.photo = photo_path
                path = os.path.join(settings.MEDIA_ROOT, 'elderly', photo.name)
                with open(path, 'wb') as pic:
                    for p in photo.chunks():
                        pic.write(p)
            one.save()
            print('save')
        label = {}
        label["page1"] = "current_page"
        label["title"] = "老人信息管理"

        elderlyList = []
        cursor = connection.cursor();
        cursor.execute('select * from veision1_elderlyinfo')
        elderlyList += dictfetchall(cursor);
        print("老人")
        print(elderlyList)

        data = render_to_string("elderly_information.html", {'elderlyList': elderlyList})
        label["data"] = data
        return render(request, "index.html", label, )

    id = request.GET.get('elderly_id')
    print("id")
    print(id)
    cursor = connection.cursor();
    elderly_info = []
    elderly_info += dictfetchall(cursor.execute('select * from veision1_elderlyinfo where id = \'{}\''.format(id)))
    print("elderly_info")
    print(elderly_info)
    print("跳转")
    return render(request, "modify_elderly.html",{'elderly_info': elderly_info[0]})

# 搜索查看工作人员
@csrf_exempt
def staff_information_management(request):
    label = {}
    label["page1"] = "current_page"
    label["title"] = "工作人员信息管理"
    staffList = []
    cursor = connection.cursor();

    if request.method == "POST":
        print("搜索")
        if request.POST.get('if_search') == "search":
            search_info = request.POST.get('staff_search_info')
            if search_info:
                staffList += dictfetchall(
                    cursor.execute('select * from veision1_staffinfo where name LIKE \'%{}%\''.format(search_info)))
                staffList += dictfetchall(cursor.execute(
                    'select * from veision1_staffinfo where id_card LIKE \'%{}%\''.format(search_info)))
                print("搜索")
                print(staffList)
            else:
                staffList += dictfetchall(cursor.execute('select * from veision1_staffinfo'))
                print("搜索")
                print(staffList)
            data = render_to_string("staff_information.html",
                                    {'staffList': staffList, 'search_info': search_info})
            label["data"] = data
            return render(request, "index.html", label)

    cursor.execute('select * from veision1_staffinfo')
    staffList += dictfetchall(cursor);
    print("工作人员")
    print(staffList)

    data = render_to_string("staff_information.html", {'staffList': staffList})
    label["data"] = data
    return render(request, "index.html", label, )

# 添加工作人员
@csrf_exempt
def add_staff(request):
    if request.method== "POST":
        print("增加工作人员")
        # 拿到提交的表单
        form = {}
        for element in request.POST:
            if element == "csrfmiddlewaretoken":
                continue
            form[element] = request.POST[element]

        photo = request.FILES.get('photo')
        print("")
        print(photo)
        path = os.path.join(settings.MEDIA_ROOT, 'staff',photo.name)
        with open(path, 'wb') as pic:
            for p in photo.chunks():
                pic.write(p)
        form["photo"] = "../static/media/staff/" + photo.name

        s = models.staffInfo.objects.create(**form)
        s.save()

        label = {}
        label["page1"] = "current_page"
        label["title"] = "工作人员信息管理"
        staffList = []
        cursor = connection.cursor();
        cursor.execute('select * from veision1_staffinfo')
        staffList += dictfetchall(cursor);
        data = render_to_string("staff_information.html", {'staffList': staffList})
        label["data"] = data
        return render(request, "index.html", label, )
    return render(request, "add_staff.html")

# 删除工作人员
def delete_staff(request):
    if request.method == 'GET':
        print("执行删除")
        id = request.GET['staff_id']
        print(id)
        cursor = connection.cursor();
        cursor.execute('delete from veision1_staffinfo where id = \'{}\''.format(id))
        res = {}
        res['cool'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')

# 修改工作人员
def modify_staff(request):
    if request.method == "POST":
        cursor = connection.cursor()
        id = request.POST.get('id')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        phone_number = request.POST.get('phone_number')
        id_card = request.POST.get('id_card')
        age = request.POST.get('age')
        photo = request.FILES.get('photo')
        one = models.staffInfo.objects.get(id=id)
        if one:
            one.name = name
            one.sex = sex
            one.phone_number = phone_number
            one.id_card = id_card
            one.age = age
            if photo:
                photo_path = "../static/media/staff/"+photo.name
                print("photopath")
                print(photo_path)
                one.photo = photo_path
                path = os.path.join(settings.MEDIA_ROOT, 'staff', photo.name)
                with open(path, 'wb') as pic:
                    for p in photo.chunks():
                        pic.write(p)
            one.save()
            print('save')
        label = {}
        label["page1"] = "current_page"
        label["title"] = "工作人员"

        staffList = []
        cursor = connection.cursor();
        cursor.execute('select * from veision1_staffinfo')
        staffList += dictfetchall(cursor);
        print("老人")
        print(staffList)

        data = render_to_string("staff_information.html", {'staffList': staffList})
        label["data"] = data
        return render(request, "index.html", label, )

    id = request.GET.get('staff_id')
    print("id")
    print(id)
    cursor = connection.cursor();
    staff_info = []
    staff_info += dictfetchall(cursor.execute('select * from veision1_staffinfo where id = \'{}\''.format(id)))
    print("staff_info")
    print(staff_info)
    print("跳转")
    return render(request, "modify_staff.html",{'staff_info': staff_info[0]})


# 搜索查看义工
@csrf_exempt
def volunteer_information_management(request):
    label = {}
    label["page1"] = "current_page"
    label["title"] = "义工信息管理"

    volunteerList = []
    cursor = connection.cursor();
    print(request.method)

    if request.method == "POST":
        print("搜索")
        if request.POST.get('if_search') == "search":
            search_info = request.POST.get('volunteer_search_info')
            if search_info:
                volunteerList += dictfetchall(
                    cursor.execute('select * from veision1_volunteerinfo where name LIKE \'%{}%\''.format(search_info)))
                volunteerList += dictfetchall(cursor.execute(
                    'select * from veision1_volunteerinfo where id_card LIKE \'%{}%\''.format(search_info)))
                print("搜索")
                print(volunteerList)
            else:
                volunteerList += dictfetchall(cursor.execute('select * from veision1_volunteerinfo'))
                print("搜索")
                print(volunteerList)
            data = render_to_string("volunteer_information.html",
                                    {'volunteerList': volunteerList, 'search_info': search_info})
            label["data"] = data
            return render(request, "index.html", label)

    cursor.execute('select * from veision1_volunteerinfo')
    volunteerList += dictfetchall(cursor);
    print("义工")
    print(volunteerList)

    data = render_to_string("volunteer_information.html", {'volunteerList': volunteerList})
    label["data"] = data
    return render(request, "index.html", label, )


# 添加义工
@csrf_exempt
def add_volunteer(request):
    if request.method== "POST":
        print("增加义工")
        # 拿到提交的表单
        form = {}
        for element in request.POST:
            if element == "csrfmiddlewaretoken":
                continue
            form[element] = request.POST[element]

        photo = request.FILES.get('photo')
        print("")
        print(photo)
        path = os.path.join(settings.MEDIA_ROOT, 'volunteer',photo.name)
        with open(path, 'wb') as pic:
            for p in photo.chunks():
                pic.write(p)
        form["photo"] = "../static/media/volunteer/" + photo.name

        s = models.volunteerInfo.objects.create(**form)
        s.save()

        label = {}
        label["page1"] = "current_page"
        label["title"] = "义工信息管理"
        volunteerList = []
        cursor = connection.cursor();
        cursor.execute('select * from veision1_volunteerinfo')
        volunteerList += dictfetchall(cursor);
        data = render_to_string("volunteer_information.html", {'volunteerList': volunteerList})
        label["data"] = data
        return render(request, "index.html", label, )
    return render(request, "add_volunteer.html")

# 删除义工
def delete_volunteer(request):
    if request.method == 'GET':
        print("执行删除")
        id = request.GET['volunteer_id']
        print(id)
        cursor = connection.cursor();
        cursor.execute('delete from veision1_volunteerinfo where id = \'{}\''.format(id))
        res = {}
        res['cool'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')

# 修改义工
def modify_volunteer(request):
    label = {}
    label["page1"] = "current_page"
    label["title"] = "义工信息管理"
    print(request.method)
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        phone_number = request.POST.get('phone_number')
        id_card = request.POST.get('id_card')
        age = request.POST.get('age')
        photo = request.FILES.get('photo')
        one = models.volunteerInfo.objects.get(id=id)
        if one:
            one.name = name
            one.sex = sex
            one.phone_number = phone_number
            one.id_card = id_card
            one.age = age
            if photo:
                photo_path = "../static/media/volunteer/"+photo.name
                print("photopath")
                print(photo_path)
                one.photo = photo_path
                path = os.path.join(settings.MEDIA_ROOT, 'volunteer', photo.name)
                with open(path, 'wb') as pic:
                    for p in photo.chunks():
                        pic.write(p)
            one.save()
            print('save')

        label = {}
        label["page1"] = "current_page"
        label["title"] = "义工信息管理"

        volunteerList = []
        cursor = connection.cursor();
        cursor.execute('select * from veision1_volunteerinfo')
        volunteerList += dictfetchall(cursor);
        print("义工")
        print(volunteerList)

        data = render_to_string("volunteer_information.html", {'volunteerList': volunteerList})
        label["data"] = data
        return render(request, "index.html", label, )

    id = request.GET.get('volunteer_id')
    print("id")
    print(id)
    cursor = connection.cursor();
    volunteer_info = []
    volunteer_info += dictfetchall(cursor.execute('select * from veision1_volunteerinfo where id = \'{}\''.format(id)))
    print("volunteer_info")
    print(volunteer_info)
    print("跳转")
    return render(request, "modify_volunteer.html",{'volunteer_info': volunteer_info[0]})

def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]



