# -*- coding: utf-8 -*-
from django.conf import settings
from users import models


def init_permission(request, user):
    """
    用户权限信息初始化，获取当前用户所有权限信息，并保存到Session中
    此处的request以及user参数均为对象，user为登陆成功时在数据库中查询到的user对象
    :param request:
    :param user:
    :return:
    """

    # TODO: 待确定，逐一取值还是传一个对象
    # 给session存好值      --   根据需求来
    request.session["username"] = user.username
    request.session["user_id"] = user.id
    request.session["email"] = user.email
    request.session["is_lock"] = user.is_lock
    request.session["is_superuser"] = True if user.role.all().filter(role="administrator") else False

    # 如果取得值很多，可以：
    # request.session["user"] = user

    # 检测用户是否被封禁：
    if request.session["is_lock"]:
        permission_list = models.Role.objects.filter(name=user.username).values(
            'groups_id',
            'groups__name',
            'groups__permissions__url',
            'groups__permissions__code',
        ).distinct()
    else:
        permission_list = user.role.all().values('groups__id', 'groups__name', 'groups__permissions__url',"groups__permissions__code").distinct()

    # 获取权限url列表
    permission_url_list = [item['groups__permissions__url'] for item in permission_list]

    # 获取权限码字典
    code_dict = {}
    for item in permission_list:
        # 也可以用权限组名字为键
        temp_dict = code_dict.setdefault(item["groups__id"], {})
        temp_dict.setdefault("id", item["groups__id"])
        temp_dict.setdefault("name", item["groups__name"])
        temp_dict.setdefault("code_list", []).append(item["groups__permissions__code"])

    request.session[settings.PERMISSION_CODE_KEY] = code_dict
    request.session[settings.PERMISSION_URL_KEY] = permission_url_list
