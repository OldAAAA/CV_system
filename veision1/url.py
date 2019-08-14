"""Web_End URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from veision1 import worker1_view
from veision1 import worker2_view
urlpatterns = [
    path("login",worker1_view.login),
    path("index",worker1_view.index),
    path("add_information",worker1_view.add_information),
    path("emotion_detection",worker2_view.emotion_detection),
    path("stranger_detection",worker2_view.stranger_detection),
    path("volunteer_interaction_detection",worker2_view.volunteer_interaction_detection),
    path("fall_detection",worker2_view.fall_detection),
    path("intrusion_detection",worker2_view.intrusion_detection),

    path("elderly_information_management",worker2_view.elderly_information_management),
    path("staff_information_management",worker2_view.staff_information_management),
    path("volunteer_information_management",worker2_view.volunteer_information_management),

    path("add_elderly",worker2_view.add_elderly),
    path("delete_elderly",worker2_view.delete_elderly),
    path("modify_elderly",worker2_view.modify_elderly),

    path("add_staff",worker2_view.add_staff),
    path("delete_staff",worker2_view.delete_staff),
    path("modify_staff",worker2_view.modify_staff),

    path("add_volunteer",worker2_view.add_volunteer),
    path("delete_volunteer",worker2_view.delete_volunteer),
    path("modify_volunteer",worker2_view.modify_volunteer),


    path("get_information",worker1_view.get_information),
    path("fix_information",worker1_view.fix_information),
    path("logout",worker1_view.logout1),
    path("create_user",worker1_view.create_user1),
    path("just_for_test",worker1_view.just_for_test),
    path("video",worker1_view.video_page),
    path("get_video",worker1_view.get_video),

    path("get_face",worker1_view.get_face)
    # path("post_photo")
]
