# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Junction, Qi
# Register your models here.

admin.site.register(Qi)
admin.site.register(Junction)