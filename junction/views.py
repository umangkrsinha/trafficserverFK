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
	
	if request.method =='POST':
		
		data = JSONParser().parse(request)

		junctionNum = data['QInfo'][0]['junctionNum']
		junction = Junction.objects.get(junctionNum = junctionNum)
		if junction.visitNum <= 3:
			junction.visitNum += 1
			junction.save()
			message = 'waiting for ' +str(4-junction.visitNum) + 'more devices!'
		
		for vehicleData in data['QInfo']:
			vehicleData.jucntionNum = junction
			serailizer = QiSerializer(data = vehicleData)
			
			if serializer.is_valid():
				serializer.save()

		if junction.visitNum >= 4:
			makePhase(junction)
			message = 'next phase has been set!'

		return JSONResponse({recievedQInfo: data['QInfo'], message: message, phase: junction.green}, status = 201)
	
	else:
		return HttpResponse('<h1>Request is not a Post request!</h1>')

def index(request):

	return HttpResponse('<h1>This is the junction app!</h1>')


def makePhase(junction):

	Q = Qi.objects.filter(junctionNum = junction)
	Q = [Q.filter(1), Q.filter(2), Q.filter(3), Q.filter(4)]
	Qlen = [len(Q[0]), len(Q[1]), len(Q[2]), len(Q[3])]

	if junction.isFirstPhase:
		junction.green = Qlen.index(max(Qlen)) + 1

	else:
		green = junction.green
		for k in [1, 2, 3, 4].remove(green):
			Qij += [len([i for i in Q[green-1] for j in Q[k-1] if i['macadd'] == j['macadd']])]

		if green == 1:
			Qlen[1] -= Qij[0]
			Qlen[2] -= Qij[1]
			Qlen[3] -= Qij[2]
			Qlen[0] -= (Qij[0] + Qij[1] + Qij[2])
			junction.Qab = (float(Qij[0])/((junction.QaNum)))*Qlen[0]
			junction.Qac = (float(Qij[1])/((junction.QaNum)))*Qlen[0]
			junction.Qad = (float(Qij[2])/((junction.QaNum)))*Qlen[0]
	    
		elif green == 2:
			Qlen[0] -= Qij[0]
			Qlen[2] -= Qij[1]
			Qlen[3] -= Qij[2]
			Qlen[1] -= (Qij[0] + Qij[1] + Qij[2])
			junction.Qba = (float(Qij[0])/((junction.QbNum)))*Qlen[1]
			junction.Qbc = (float(Qij[1])/((junction.QbNum)))*Qlen[1]
			junction.Qbd = (float(Qij[2])/((junction.QbNum)))*Qlen[1]	
		elif green == 3:
			Qlen[0] -= Qij[0]
			Qlen[1] -= Qij[1]
			Qlen[3] -= Qij[2]
			Qlen[2] -= (Qij[0] + Qij[1] + Qij[2])
			junction.Qca = (float(Qij[0])/((junction.QcNum)))*Qlen[2]
			junction.Qcb = (float(Qij[1])/((junction.QcNum)))*Qlen[2]
			junction.Qcd = (float(Qij[2])/((junction.QcNum)))*Qlen[2]
		else:
			Qlen[0] -= Qij[0]
			Qlen[1] -= Qij[1]
			Qlen[2] -= Qij[2]
			Qlen[3] -= (Qij[0] + Qij[1] + Qij[2])
			junction.Qda = (float(Qij[0])/((junction.QdNum)))*Qlen[3]
			junction.Qdb = (float(Qij[1])/((junction.QdNum)))*Qlen[3]
			junction.Qdc = (float(Qij[2])/((junction.QdNum)))*Qlen[3]

	junction.QaNum,  junction.QbNum, junction.QcNum, junction.QdNum = Qlen[0], Qlen[1], Qlen[2], Qlen[3]
	junction.visitNum = 0
	
	if junction.isFirstPhase:
		junction.isFirstPhase = False
		junction.save()
		return 0

	junction.green = algo(junction)
	junction.save()
	return 0
	
#the main algorhithm: returns the number of the road which should have green light for the next phase
def algo(junction):
	return 1 #green light should be on road a

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