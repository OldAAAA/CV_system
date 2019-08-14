from django.db.models import Count

from demo.models import Eventinfo


def emotion_operation():
    # 查询数据库，生成情绪信息报表
    # 筛选出愤怒、高兴、中性的信息
    handle = Eventinfo.objects.filter(type=0, description="happy", ).values("name", "description").annotate(
        num_name=Count("description"))
    handle1 = Eventinfo.objects.filter(type=0, description="angry", ).values("name", "description").annotate(
        num_name=Count("description"))
    handle2 = Eventinfo.objects.filter(type=0, description="neutral", ).values("name", "description").annotate(
        num_name=Count("description"))

    # 拼接形成列表
    count = handle.count()
    count1 = handle1.count()
    count2 = handle2.count()

    data = {}

    data["elderlyList"] = ["0"] * (count + count1 + count2)
    data["elderlyHappyList"] = ["0"] * (count + count1 + count2)
    data["elderlyAngryList"] = ["0"] * (count + count1 + count2)
    data["elderlyNeutralList"] = ["0"] * (count + count1 + count2)

    # 记录老人的数量
    count = 0
    # 记录老人情绪的次数
    count1 = 0
    # 记录老人情绪的次数
    count2 = 0

    for item in handle:
        data["elderlyList"][count] = item["name"]
        count += 1
        data["elderlyHappyList"][count1] = item["num_name"]
        count1 += 1
    print(data["elderlyList"])

    print("count1:"+str(count1))

    for item in handle1:
        if item["name"] in data["elderlyList"]:
            index = data["elderlyList"].index(item["name"])
        else:
            data["elderlyList"][count] = item["name"]
            index = data["elderlyList"].index(item["name"])
            count += 1
        data["elderlyAngryList"][index] = item["num_name"]
        count2 += 1

    print("count2:" + str(count2))
    if count2 > count1:
        count1 = count2


    count2 = 0
    for item in handle2:
        if item["name"] in data["elderlyList"]:
            index = data["elderlyList"].index(item["name"])
        else:
            data["elderlyList"][count] = item["name"]
            index = data["elderlyList"].index(item["name"])
            count += 1
        data["elderlyNeutralList"][index] = item["num_name"]
        count2 += 1

    print("count2:" + str(count2))
    if count2 > count1:
        count1 = count2

    print(count1)

    # 删除不必要的元素
    print(data["elderlyList"])
    print(data["elderlyHappyList"])
    print(data["elderlyAngryList"])
    print(data["elderlyNeutralList"])
    data["elderlyList"] = [data["elderlyList"][i] for i in range((count))]
    data["elderlyHappyList"] = [data["elderlyHappyList"][i] for i in range((count1))]
    data["elderlyAngryList"] = [data["elderlyAngryList"][i] for i in range((count1))]
    data["elderlyNeutralList"] = [data["elderlyNeutralList"][i] for i in range((count1))]

    print(data["elderlyList"])
    print(data["elderlyHappyList"])
    print(data["elderlyAngryList"])
    print(data["elderlyNeutralList"])

    return data