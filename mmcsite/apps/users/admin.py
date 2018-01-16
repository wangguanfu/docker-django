# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Permissions, Role, PermissionsGroup,CompanyProfile

# Register your models here.

admin.site.register(User)
admin.site.register(PermissionsGroup)
admin.site.register(Permissions)
admin.site.register(Role)
admin.site.register(CompanyProfile)


