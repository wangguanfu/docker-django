# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from users import models
from users.services import rbac
from django.utils import timezone
from django.db.models import Q
from mmcsite import settings
# TODO: 用于事务操作
from django.db import transaction
import datetime
import hashlib


def index(request):#首頁
    if request.method == "GET":
        return JsonResponse({"result": 0, "message": "Everyone can visit."})


def login(request):
    if request.method == "GET":
        return render(request,"login.html")
        # return JsonResponse({"result": 0, "message": "Everyone can visit."})
    if request.method == "POST":
        # user_id = request.user.id or None
        username = request.POST.get("username")
        password = hashlib.sha1(request.POST.get("password")).hexdigest()
        email = request.POST.get("email")
        user = models.User.objects.filter(Q(username=username, password=password)|Q(email=email, password=password)).first()
        if user is None:
            # 表示用户的认证失败
            return JsonResponse({"result": 1, "message": "Username or password is incorrect"})
        else:
            # 登录成功则初始化权限信息
            rbac.init_permission(request, user)
            profile = user.profile
            models.Message.objects.create(   # 记录操作
                login_time=timezone.now(),
                username=username,
                message="%s has login in" %(username),
            )
            if request.session.get("is_superuser"):
                code_dict = request.session.get(settings.PERMISSION_CODE_KEY)
                data = {
                    'profile':profile.name,
                    'is_superuser': 1,     #1 是超级管理员　0是普通管理员
                    'code_dict': code_dict   # 权限码
                }
            if request.session["is_lock"]:
                return JsonResponse({"result": 0, "message": '您的账户被锁定了'})
            return JsonResponse({"result": 0, "message": 'success！', "data": data})


def log_out(request):#退出登陆
    request.session.flush()
    # return redirect('/users/post/')
    return JsonResponse({"result": 0, "message": "success"})


def add_user(request):
    '''
    增加用户
    :param request:
    :return:
    '''
    if request.method == "POST":
        # user = request.user
        username = request.POST.get('username', '')  # 需要修改的用户ID
        email = request.POST.get('email', '')  # 需要修改的邮箱
        is_lock = request.POST.get('is_lock', '')  # 是否要锁定
        password = hashlib.sha1(request.POST.get("password")).hexdigest()  # 需要修改的密码
        mobile = request.POST.get('mobile', '')  #
        temperature_unit = request.POST.get('TYPE', '0')  #
        note = request.POST.get('Note', '')  #
        data = models.User.objects.create(
            username=username,
            # user_id=user_id,
            email=email,
            is_lock=is_lock,
            password=password,
            mobile=mobile,
            temperature_unit=temperature_unit,
            note=note
        )
        data.save()
        models.Message.objects.create( # 记录操作
            login_time=timezone.now(),
            username=username,
            message="%s was add" % (username),
        )
        return JsonResponse({"result": 0, "message": "success"})
    return JsonResponse({"message": 'bad request', 'result': 1})


def delete_user(request,):
    '''
    删除用户
    :param request:
    :return:
    '''
    if request.method == "POST":
        username = request.POST.get('username', '')  # 需要修改的用户ID
        data = models.User.objects.filter(username=username)
        data.delete()
        return JsonResponse({"result": 0, "message": "success"})


def update_user(request):
    '''
    修改用户
    :param request:
    :return:
    '''
    if request.method == "POST":
        # user = request.POST.get('username','')
        user = request.Session.get('username')
        user_id = request.POST.get('user_id', '')  # 需要修改的用户ID
        email = request.POST.get('email', '')  # 需要修改的邮箱
        # is_lock = request.POST.get('is_lock', '')  # 是否要锁定
        password = hashlib.sha1(request.POST.get("password")).hexdigest() or '' # 需要修改的密码
        mobile = request.POST.get('mobile', '')#
        temperature_unit = request.POST.get('TYPE', '0')#
        note = request.POST.get('Note', '')#
        data = models.User.objects.filter(id =user_id)
        data.user = user
        data.user_id= user_id
        data.email =email
        # data.is_lock = is_lock
        data.password = password
        data.mobile= mobile
        data.temperature_unit =temperature_unit
        data.note = note
        data.save()
        models.Message.objects.create(  # 记录操作
            login_time=timezone.now(),
            username=user,
            message="%s has was changed" % (user),
        )
        return JsonResponse({"result": 0, "message": "success"})


def get_users(request):
    '''
    返回用户列表
    :param request:
    :return:
    '''
    # if request.method == "POST":
    users =models.User.objects.all().values()
    data = {}
    for user in users:
        # profile = models.IotProfile.objects.filter(profile_id=user['profile_id'])
        data['user'] = user
    return JsonResponse({"result": 0, "message": "success","data":data})


# 获取角色列表
def get_roles(request):
    """
    获取角色列表
    """
    # if request.method == "POST":
        # 前端传来是给哪个页面展示
    show_all = request.POST.get("show_all")
    if show_all:
        roles_list = list(models.Role.objects.all().values("id", "name"))
    else:
        # 只获取超级管理员和管理员
        roles_list = list(models.Role.objects.filter(is_show=True).values("id", "name"))

    return JsonResponse({"result": 0, "message": '角色列表', 'roles_list': roles_list})


def update_roles(request):
    """
    编辑角色
    """
    if request.method == "POST":
        # 从前台拿到修改的角色ID
        role_id = int(request.POST.get("role_id"))
        # 在数据库中找到数据
        role = models.Role.objects.filter(id=role_id).first()

        # 从前台拿到修改的权限组ID
        group_list = request.POST.getlist("group_id")

        with transaction.atomic():
            # 修改角色具有的权限
            role.groups.set(role_id, group_list)

        return JsonResponse({"result": 0, "message": "success","data":group_list})


def add_roles(request):
    """
    添加角色
    """
    if request.method == "POST":
        name = request.POST.get('name')
        group_list = request.POST.getlist("group_id")

        with transaction.atomic():
            role_obj = models.Role.objects.create(role=name, is_show=False)
            role_obj.groups.add(group_list)

        return JsonResponse({"result": 0, "message": "success"})

#
# def delete_roles(request):
#     """
#     删除角色
#     """
#     if request.method == "POST":
#
#         # 从前台拿到修改的角色ID
#         role_id = int(request.POST.get("role_id"))
#         # 在数据库中删除数据
#         role = models.Role.objects.filter(id=role_id).first()
#         if role:
#             models.Role.objects.filter(id=role_id).delete()
#
#         return JsonResponse({"result": 0, "message": '删除成功'})


# 返回权限组的列表
def get_groups(request):
    """
    获取权限组列表
    """
    # if request.method == "POST":
        # 前端传来是给哪个页面展示
    show_all = request.POST.get("show_all")
    if show_all:
        groups_list = list(models.PermissionsGroup.objects.all().values("id", "name"))
    else:
        # 不获取如收货发货之类的权限组
        groups_list = list(models.PermissionsGroup.objects.filter(is_show=True).values("id", "name"))
    return JsonResponse({"result": 0, "message": '权限列表', 'data': groups_list})


# # 修改权限组列表
# def update_groups(request):
#     """
#     修改权限组列表
#     """
#     if request.method == "POST":
#         # 从前台拿到修改的权限组ID
#         group_id = int(request.POST.get("group_id"))
#         # 在数据库中找到数据
#         group_obj = models.PermissionsGroup.objects.filter(id=group_id).first()
#
#         # 从前台拿到修改的权限ID
#         permission_list = request.POST.getlist("permission_id")
#
#         with transaction.atomic():
#             # 修改角色具有的权限
#             group_obj.permissions.set(group_id, permission_list)
#         return JsonResponse({"result": 0, "message": ''})


# 操作记录
def get_audit_log(request):
    """
    管理员可以查全部，普通管理员只能查自己
    :param request:
    :return:
    """
    user_id = request.session.get("user_id")
    if request.session.get("is_lock"):
        return JsonResponse({"message": "用户被锁定"})
    if request.session.get("is_superuser"):
        # 管理员获取全部message
        log = models.Message.objects.filter(login_time=datetime.now()).values()#测试时间 分页 换算
        # values方便转化为json
    else:
        log = models.Message.objects.filter(user_id=user_id).values()
    return JsonResponse({"result":0 ,"message": "success","log":log})


def get_profile(request):
    """
        查看公司信息
       :param request:
       :return:
       """
    user_id = request.session.get("user_id")
    email = request.session.get("email")
    username = request.session.get("username")
    if request.session.get("is_superuser"):
        # 管理员获取全部公司信息
        data = models.IotProfile.objects.all().values()  # 测试时间 分页 换算
        # values方便转化为json
    else:
        data = models.Message.objects.filter(user_id=user_id).values()
    return JsonResponse({"result": 0,"message": "success", "data": data})


def edit_profile(request):
    """
    编辑公司信息
       :param request:
       :return:
       """
    user_id = request.session.get("user_id")
    email = request.session.get("email")
    # username = request.session.get("username")
    if request.session.get("is_superuser"):
        # 管理员获取全部公司信息
        data = models.IotProfile.objects.all().values()  # 测试时间 分页 换算
        # values方便转化为json
    else:
        data = models.Message.objects.filter(user_id=user_id).values()
    return JsonResponse({"result":0,"message":"sussess", "data": data})




