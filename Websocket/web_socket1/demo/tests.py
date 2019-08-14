import json
import time

import requests

# from demo.models import Eventinfo


# def get_emotion_form():
#     handle = Eventinfo.objects.filter(type = 0)




def go_emotion():
    name = ["lqw","xh","wjh"]
    data = {}
    data["name"] = name
    data["type"] = 0
    data["date"] = "2019-07-07"
    data["description"] = ["angry","happy","sad"]
    # data = json.loads(name)
    requests.post("http://127.0.0.1:9000/chat/emotion",json=data)

    print(data)

    return "emotion"

def go_interact():
    data = {"date": "2019-7-1", "name": "ylz", "description": "wjh"}
    requests.post("http://127.0.0.1:8000/chat/interact",json=data)
    print(data)

    return "Interact"

def go_fall():
    data = {"date": "2019-7-3", "name": "<null>", "description": "YF教室"}
    requests.post("http://127.0.0.1:9000/chat/fall",json=data)
    print(data)

    return "Fall"

def go_attack():
    data = {"date": "2019-7-4", "name": "<null>", "description": "YF教师"}
    requests.post("http://127.0.0.1:9000/chat/attack",json=data)
    print(data)

    return "attack"

def go_stranger():
    data = {"date": "2019-7-3", "name": "<null>", "description": "bedreom"}
    requests.post("http://127.0.0.1:9000/chat/stranger",json=data)
    print(data)

    return "stranger"



print(go_attack())
# a = []
# a =["0"] * 3
# print(a)

# a = ["1","2"]
# b = a.append("3")
# print(b)

# import random
#
# rand = [0,0,0,0,0]
#
# for i in range(5):
#     rand[i] = random.randint(4000,5000)
#
# for i in range(5):
#     print(str(rand[i]))
#
# for i in range(5):
#     print(str(1 / rand[i]))



















def localtime():
    return time.strftime("%Y-%m-%d",time.localtime(time.time()))

# print(localtime())

# def get_post():
#     request={'data':['2019-07-05 08:57:15'],}
#     for item in request:
#         data[item] =
#         for element in request.POST[item]:
#         data[item] = deepcopy(request.POST[item])

# transfor_json()
# list = ['niaho']
# list.append("nihao")