# -*- coding: utf-8 -*-
from django.shortcuts import redirect, HttpResponse
from django.http import JsonResponse
from django.conf import settings
import re


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):
    """
    权限管理中间件
    """
    def process_request(self, request):
        # 1. 当前请求URL
        current_request_url = request.path_info

        # 2. 处理白名单,如login及admin页面， 直接放行
        for url in settings.VALID_URL_LIST:
            print url, current_request_url
            if re.match(ur"^{0}".format(url), current_request_url):
                return None

        # 3. 获取session中保存的权限信息
        permission_url_list = request.session.get(settings.PERMISSION_URL_KEY)
        if not permission_url_list:
            # 权限列表为空表示无任何权限
            return redirect(settings.RBAC_LOGIN_URL)

        # 4. 判断用户是否有权限访问当前请求的url
        flag = False
        for url in permission_url_list:
            if re.match("^{0}$".format(url), current_request_url):
                flag = True
                break
        if not flag:
            # 无权访问页面，可以直接redirect
            return JsonResponse({'result': 1 , "message": "No permission to visit."})



