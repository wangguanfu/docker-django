# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from device.models import IotDevice, Device, DeviceProfile
from users.models import User

from utils.views import HttpResponseMessage, HttpResponseMessageWithData, dateFormat
from django.http import JsonResponse
from django.db import transaction


def t_to_dict(t):
    t_dict = {
        "device_id": t.device_id,
        "mac": t.mac_addr,
        "serial_num": t.serial_num,
        "model_num": t.model_num,
        "firmware_rev": t.firmware_rev,
        "software_rev": t.software_rev,
        "hardware_rev": t.hardware_rev,
        # 新添加
        # "profiles": t.profiles,
    }
    return t_dict


# mmc APIs for device
@csrf_exempt
def register(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'mac' in json_data:
        _mac = json_data['mac']
    else:
        return HttpResponseMessage(1, 'no mac in request')

    try:
        device = IotDevice.objects.get(mac_addr=_mac)
    except:
        if 'serial_num' in json_data:
            _number = json_data['serial_num']

        if 'model_num' in json_data:
            _model = json_data['model_num']

        if 'firmware_rev' in json_data:
            _fm_rev = json_data['firmware_rev']

        if 'software_rev' in json_data:
            _sw_rev = json_data['software_rev']

        if 'hardware_rev' in json_data:
            _hw_rev = json_data['hardware_rev']

        # TODO:待测试
        # if 'profiles' in json_data:
        #     _profiles = json_data["profiles"]

        device = IotDevice.objects.create(
            mac_addr=_mac,
            serial_num=_number,
            model_num=_model,
            firmware_rev=_fm_rev,
            software_rev=_sw_rev,
            hardware_rev=_hw_rev,
            # 新添加
            # profiles=_profiles,
        )

    return HttpResponseMessageWithData(0, 'success', "device_id", device.device_id)


@csrf_exempt
def update(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'mac' in json_data:
        _mac = json_data['mac']
    else:
        return HttpResponseMessage(1, 'no mac in request')

    try:
        device = IotDevice.objects.get(mac_addr=_mac)
        changed = False
        if 'serial_num' in json_data:
            _number = json_data['serial_num']
            if _number != device.serial_num:
                device.serial_num = _number
                changed = True

        if 'model_num' in json_data:
            _model = json_data['model_num']
            if _model != device.model_num:
                device.model_num = _model
                changed = True

        if 'firmware_rev' in json_data:
            _fm_rev = json_data['firmware_rev']
            if _fm_rev != device.firmware_rev:
                device.firmware_rev = _fm_rev
                changed = True

        if 'software_rev' in json_data:
            _sw_rev = json_data['software_rev']
            if _sw_rev != device.software_rev:
                device.software_rev = _sw_rev
                changed = True

        if 'hardware_rev' in json_data:
            _hw_rev = json_data['hardware_rev']
            if _hw_rev != device.hardware_rev:
                device.hardware_rev = _hw_rev
                changed = True

        # TODO:待测试
        # if 'profiles' in json_data:
        #     _profiles = json_data['profiles']
        #     if _profiles != device.profiles:
        #         device.profiles = _profiles
        #         changed = True

        if changed:
            device.save()
        return HttpResponseMessageWithData(0, 'success', "device_id", device.device_id)
    except:
        return HttpResponseMessage(1, 'the mac not in db')


# csrfmiddlewaretoken: "{{ csrf_token }}"
@csrf_exempt
def get(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
    else:
        return HttpResponseBadRequest('Bad Request')

    if 'device_id' in json_data:
        _device_id = json_data['device_id']
        try:
            device = IotDevice.objects.get(device_id=_device_id)
            return HttpResponseMessageWithData(0, 'success', "device", t_to_dict(device))
        except:
            return HttpResponseMessage(1, 'not a valid device id')

    if 'mac' in json_data:
        _mac = json_data['mac']
        try:
            device = IotDevice.objects.get(mac_addr=_mac)
            return HttpResponseMessageWithData(0, 'success', "device", t_to_dict(device))
        except:
            return HttpResponseMessage(2, 'the mac is not saved')

    return HttpResponseMessage(3, 'no device id or mac in request')


def get_device(request):
    """
    获取设备列表
    :param request:
    :return:
    """
    if request.method == "POST":

        if request.session.get("is_superuser"):
            device_list = Device.objects.all().select_related("profile")
        else:
            user = User.objects.filter(id=request.session.get("user_id")).first()
            device_list = user.device_set.all().select_related("profile")
        # 获取设备数据组装成字典
        device_data_list = []
        for row in device_list:
            device_data_list.append({
                "SN": row.SN,
                "state": row.state,
                "profile_name": row.profile.name,
                "users": [item.username for item in row.users.all()],
                "model": row.model,
            })

        return JsonResponse({"result": 0, "message": "success", "data": device_data_list})


def add_device(request):
    """
    添加设备
    :param request:
    :return:
    """
    if request.method == "POST":
        SN = request.POST.get("SN")
        profile_name = request.POST.get("profile_name")
        user_id_list = request.POST.getlist("users")
        # create_time = request.POST.get("create_time")     # 新增时自动生成

        with transaction.atomic():
            device = Device.objects.create(SN=SN)
            device.users.add(user_id_list)
            device.profile = DeviceProfile(name=profile_name)

        return JsonResponse({"result": 0, "message": "Add device successfully."})


def edit_device(request):
    """
    编辑设备
    :param request:
    :return:
    """
    if request.method == "POST":
        device_id = request.POST.get("device_id")
        SN = request.POST.get("SN")
        profile_name = request.POST.get("profile_name")
        user_id_list = request.POST.getlist("users")
        # TODO：这里需要对时间进行处理
        create_time = request.POST.get("create_time")

        # 验证身份
        device = Device.objects.filter(id=device_id).first()
        if not device:
            return JsonResponse({"result": 1, "message": "Device not found."})
        if not request.session.get("is_superuser") or not device.users.filter(id=request.session.get("user_id")):
            return JsonResponse({"result": 2, "message": "No permission to operate this device."})

        with transaction.atomic():
            device.SN = SN
            device.create_time = create_time
            device.users.set(user_id_list)
            device.profile.name = profile_name

            device.save()
            device.profile.save()

        return JsonResponse({"result": 0, "message": "Edit device successfully."})


def edit_profile(request):
    """
    编辑设备设置
    :param request:
    :return:
    """
    if request.method == "POST":
        profile_id = request.POST.get("profile_id")
        profile_name = request.POST.get("profile_name")
        device_type = request.POST.get("device_type")
        describe = request.POST.get("describe")
        delayed = request.POST.get("delayed")
        record_interval = request.POST.get("record_interval")
        high_temperature = request.POST.get("high_temperature")
        low_temperature = request.POST.get("low_temperature")
        # TODO：这里需要对时间进行处理
        create_time = request.POST.get("create_time")

        # 验证身份
        profile = DeviceProfile.objects.filter(id=profile_id).first()
        if not profile:
            return JsonResponse({"result": 1, "message": "Profile not found."})
        if not request.session.get("is_superuser") or not profile.device.users.filter(id=request.session.get("user_id")):
            return JsonResponse({"result": 2, "message": "No permission to operate this profile."})

        with transaction.atomic():
            profile.name = profile_name
            profile.type = device_type
            profile.describe = describe
            profile.delayed = delayed
            profile.record_interval = record_interval
            profile.high_temperature = high_temperature
            profile.low_temperature = low_temperature
            profile.create_time = create_time

            profile.save()

        return JsonResponse({"result": 0, "message": "Edit profile successfully."})


def add_profile(request):
    """
    添加设备设置
    :param request:
    :return:
    """
    if request.method == "POST":
        profile_name = request.POST.get("profile_name")
        device_type = request.POST.get("device_type")
        describe = request.POST.get("describe")

        delayed = request.POST.get("delayed")
        record_interval = request.POST.get("record_interval")
        high_temperature = request.POST.get("high_temperature")
        low_temperature = request.POST.get("low_temperature")

        DeviceProfile.objects.create(
            name=profile_name,
            type=device_type,
            describe=describe,
            delayed=delayed,
            record_interval=record_interval,
            high_temperature=high_temperature,
            low_temperature=low_temperature
        )

        return JsonResponse({"result": 0, "message": "Add profile successfully."})

# 查询
def search(request):
    if request.session.get("is_superuser"):
        device_list = Device.objects.all().select_related("profile")
    else:
        user = User.objects.filter(id=request.session.get("user_id")).first()
        device_list = user.device_set.all().select_related("profile")
        # 获取设备数据组装成字典
    if request.POST.get("model"):

        # 按是否激活搜索
        model = request.POST.get("model")
        device_lists = device_list.filter(model=model)
    elif request.POST.get("time"):
        # 按时间搜索
        time = request.POST.get("time")
        device_lists = device_list.filter(create_time=time)
    elif request.POST.get("words"):
        # 按名字，自定义字段，简介模糊搜索
        words = request.POST.get("words")

        from django.db.models import Q
        condition = Q()
        condition.connector = "OR"
        for con in ["profile__name", "customer_field__content", "profile__describe"]:
            condition.children.append("{0}__contains".format(con), words)

        device_lists = device_list.filter(condition)

    return JsonResponse({"result": 0, "message": "success", "device_lists": device_lists})

















