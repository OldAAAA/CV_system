import copy
import json
from copy import deepcopy

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe

from demo.database_operation import emotion_operation
from demo.models import Eventinfo


def index(request):
    return render(request, 'index.html')

def room(request, room_name):
    print(room_name)
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

#接受来自cv端的情绪检测的数据
def emotion(request):
    channel_layer = get_channel_layer()

    # 解析CV端穿过来的信息，交互信息包括
    body = request.body
    a = json.loads(body)

    # 将发过来的信息进行保存，保存到本地的数据库
    data = {}

    count = 0
    message = []
    for item in a["name"]:
        # 生成一条数据库信息
        data["date"] = a["date"]
        data["description"] = a["description"][count]
        data["name"] = item
        data["type"] = 0
        count += 1
        print(data)

        #将数据保存到数据库中
        handle = Eventinfo.objects.create(**data)
        handle.save()

        message.append(data["date"] + " " + data["name"] + " " + data["description"])

    data = emotion_operation()

    # 情绪标签加上消息服务器开启信息
    data["label"] = 0
    data["message"] = message


    async_to_sync(channel_layer.group_send)(
        "chat_emotion",
        {
            'type': 'chat_message',
            'message': data
        }
    )

    return HttpResponse("ok")

#初始化发送情绪检测的数据
def send_static_emition():
    data = emotion_operation()

    data["label"] = 0
    data["message"] = ["消息服务器连接成功","开始监听"]

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "chat_emotion",
        {
            'type': 'chat_message',
            'message': data
        }
    )

#接受来自cv端的交互检测的数据
def interact(request):
    channel_layer = get_channel_layer()

    #解析CV端穿过来的信息，交互信息包括
    body = request.body
    a = json.loads(body)

    #将发过来的信息进行保存，保存到本地的数据库
    data = {}

    #生成一条数据库信息
    data["date"] = a["date"]
    data["description"] = a["description"]
    data["name"] = a["name"]
    data["type"] = 1
    message = [str(data["date"]) + " " + data["name"][0] + "和" + data["description"][0]+"发生了一次交互"]

    #将数据保存到数据库中
    handle = Eventinfo.objects.create(**data)
    handle.save()

    #从数据库中读取历史数据进行发送
    # 筛选出高兴、悲伤的信息
    handle = Eventinfo.objects.filter(type=1).values("name", "description").annotate(num=Count("description"))

    data = {}
    data["elderlyList"] = []
    data["volunteerList"] = []
    data["elderlyInteractionList"] = []
    data["label"] = 1
    data["message"] =[]
    data["message"].append(message)

    for item in handle:
        if item["name"] not in data["elderlyList"]:
            data["elderlyList"].append(item["name"])
        if item["description"] not in data["volunteerList"]:
            data["volunteerList"].append(item["description"])
        x = data["elderlyList"].index(item["name"])
        y = data["volunteerList"].index(item["description"])
        data["elderlyInteractionList"].append([y,x,item["num"]])

    print(data["elderlyList"])
    print(data["volunteerList"])
    print(data["elderlyInteractionList"])

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "chat_interact",
        {
            'type': 'chat_message',
            'message': data
        }
    )
    return HttpResponse("interact")

#初始化发送交互检测的数据
def sned_interact_static():
    channel_layer = get_channel_layer()

    # 从数据库中读取历史数据进行发送
    # 筛选出高兴、悲伤的信息
    handle = Eventinfo.objects.filter(type=1).values("name", "description").annotate(num=Count("description"))

    data = {}
    data["elderlyList"] = []
    data["volunteerList"] = []
    data["elderlyInteractionList"] = []
    data["label"] = 1
    data["message"] = ["消息服务器连接成功", "开始监听"]

    for item in handle:
        if item["name"] not in data["elderlyList"]:
            data["elderlyList"].append(item["name"])
        if item["description"] not in data["volunteerList"]:
            data["volunteerList"].append(item["description"])
        x = data["elderlyList"].index(item["name"])
        y = data["volunteerList"].index(item["description"])
        data["elderlyInteractionList"].append([y, x, item["num"]])

    print(data["elderlyList"])
    print(data["volunteerList"])
    print(data["elderlyInteractionList"])

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "chat_interact",
        {
            'type': 'chat_message',
            'message': data
        }
    )

#接受来自cv端的陌生个人检测的数据
def stranger(request):
    channel_layer = get_channel_layer()

    # 解析CV端穿过来的信息，交互信息包括
    body = request.body
    a = json.loads(body)

    # 将发过来的信息进行保存，保存到本地的数据库
    data = {}

    # 生成一条数据库信息
    data["date"] = a["date"]
    data["description"] = a["description"]
    data["name"] = a["name"]
    data["type"] = 2
    message = [data["date"][0] + " " + "在" + data["description"][0] + "有人入侵，警告警告！！"]
    print(message)

    # 将数据保存到数据库中
    handle = Eventinfo.objects.create(**data)
    handle.save()

    # 从数据库中读取历史数据进行发送
    # 筛选出高兴、悲伤的信息
    handle = Eventinfo.objects.filter(type=2).values("date").annotate(num=Count("name"))

    data["dateList"] = []
    data["strangerNumList"] = []
    data["label"] = 2
    data["message"] = message

    for item in handle:
        data["dateList"].append(str(item["date"]))
        data["strangerNumList"].append(item["num"])
        print(str(item["date"]) + "  " + str(item["num"]))

    # Send message to room group
    async_to_sync(channel_layer.group_send)(
        "chat_stranger",
        {
            'type': 'chat_message',
            'message': data
        }
    )
    return HttpResponse("ok")

#初始化发送陌生人检测的数据
def send_stranger_static():
    channel_layer = get_channel_layer()

    data = {}
    # 从数据库中读取历史数据进行发送
    # 筛选出高兴、悲伤的信息
    handle = Eventinfo.objects.filter(type=2).values("date").annotate(num=Count("name"))

    data["dateList"] = []
    data["strangerNumList"] = []
    data["label"] = 2
    data["message"] = ["消息服务器连接成功", "开始监听"]

    for item in handle:
        data["dateList"].append(str(item["date"]))
        data["strangerNumList"].append(item["num"])
        print(str(item["date"]) + "  " + str(item["num"]))

    # Send message to room group
    async_to_sync(channel_layer.group_send)(
        "chat_stranger",
        {
            'type': 'chat_message',
            'message': data
        }
    )

#接受来自cv端的摔倒检测的数据
def fall(request):
    channel_layer = get_channel_layer()
    data = {}

    # 解析CV端穿过来的信息，交互信息包括
    body = request.body
    a = json.loads(body)

    # 将发过来的信息进行保存，保存到本地的数据库
    data = {}

    # 生成一条数据库信息
    data["date"] = a["date"]
    data["description"] = a["description"]
    data["name"] = a["name"]
    data["type"] = 3
    message = [data["date"] + " " + "在" + data["description"] + "有人摔倒了，警告警告！！"]
    print(message)



    # 将数据保存到数据库中
    handle = Eventinfo.objects.create(**data)
    handle.save()

    # 从数据库中读取历史数据进行发送
    # 筛选出高兴、悲伤的信息
    handle = Eventinfo.objects.filter(type=3).values("date").annotate(num=Count("name"))

    data["dateList"] = []
    data["fallNumList"] = []
    data["label"] = 3
    data["message"] = message

    for item in handle:
        data["dateList"].append(str(item["date"]))
        data["fallNumList"].append(item["num"])
        print(str(item["date"]) + "  " +str(item["num"]))

    # Send message to room group
    async_to_sync(channel_layer.group_send)(
        "chat_fall",
        {
            'type': 'chat_message',
            'message': data
        }
    )
    return HttpResponse("ok")

#初始化发送摔倒检测的数据
def send_fall_static():
    channel_layer = get_channel_layer()

    data = {}
    # 从数据库中读取历史数据进行发送
    # 筛选出高兴、悲伤的信息
    handle = Eventinfo.objects.filter(type=3).values("date").annotate(num=Count("name"))

    data["dateList"] = []
    data["fallNumList"] = []
    data["label"] = 3
    data["message"] = ["消息服务器连接成功", "开始监听"]

    for item in handle:
        data["dateList"].append(str(item["date"]))
        data["fallNumList"].append(item["num"])
        print(str(item["date"]) + "  " + str(item["num"]))

    # Send message to room group
    async_to_sync(channel_layer.group_send)(
        "chat_fall",
        {
            'type': 'chat_message',
            'message': data
        }
    )

#接受cv端闯入识别的数据
def attack(request):
    channel_layer = get_channel_layer()
    data = {}

    # 解析CV端穿过来的信息，交互信息包括
    body = request.body
    a = json.loads(body)

    # 将发过来的信息进行保存，保存到本地的数据库
    data = {}

    # 生成一条数据库信息
    data["date"] = a["date"]
    data["description"] = a["description"]
    data["name"] = a["name"]
    data["type"] = 4
    message = [data["date"] + " " + "在" + data["description"] + "老头老奶逃跑了，警告警告！！"]
    print(message)

    # 将数据保存到数据库中
    handle = Eventinfo.objects.create(**data)
    handle.save()

    # 从数据库中读取历史数据进行发送
    # 筛选出高兴、悲伤的信息
    handle = Eventinfo.objects.filter(type=4).values("date").annotate(num=Count("name"))

    data["dateList"] = []
    data["intrudeNumList"] = []
    data["label"] = 4
    data["message"] = message

    for item in handle:
        data["dateList"].append(str(item["date"]))
        data["intrudeNumList"].append(item["num"])
        print(str(item["date"]) + "  " + str(item["num"]))

    # Send message to room group
    async_to_sync(channel_layer.group_send)(
        "chat_attack",
        {
            'type': 'chat_message',
            'message': data
        }
    )
    return HttpResponse("ok")

#初始化发送闯入识别的数据
def send_attack_static():
    channel_layer = get_channel_layer()
    data={}

    # 从数据库中读取历史数据进行发送
    # 筛选出高兴、悲伤的信息
    handle = Eventinfo.objects.filter(type=4).values("date").annotate(num=Count("name"))

    data["dateList"] = []
    data["intrudeNumList"] = []
    data["label"] = 4
    data["message"] = ["消息服务器连接成功", "开始监听"]

    for item in handle:
        data["dateList"].append(str(item["date"]))
        data["intrudeNumList"].append(item["num"])
        print(str(item["date"]) + "  " + str(item["num"]))

    # Send message to room group
    async_to_sync(channel_layer.group_send)(
        "chat_attack",
        {
            'type': 'chat_message',
            'message': data
        }
    )

#测试使用的函数
def change_data(request):
    data = {}
    description = ""
    for item in request.GET:
        if item == "name" or item == "date" or item == "type":
            data[item] = request.GET[item]
        else:
            description += str(request.GET[item])
    data["description"] = description

    handle = Eventinfo.objects.create(**data)
    handle.save()

    return HttpResponse("OK")

def post_data(request):
    body = request.body
    a = json.loads(body)
    print(a["name"])
    return HttpResponse("你好")




