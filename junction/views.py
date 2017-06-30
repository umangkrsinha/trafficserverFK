# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json, decimal

from .serializers import JunctionSerializer, QiSerializer
from .models import Junction, Qi

# Create your views here.

@csrf_protect
@csrf_exempt
def upload(request):
	
	pass

def index(request):

	return HttpResponse('<h1>This is the junction app!</h1>')

#Helper functions:
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def decimal_default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError