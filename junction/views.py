# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json, decimal
import numpy
from .serializers import JunctionSerializer, QiSerializer
from .models import Junction, Qi

# Create your views here.

@csrf_protect
@csrf_exempt
def upload(request):
	
	if request.method =='POST':
		
		data = JSONParser().parse(request)

		junctionNum = data['QInfo'][0]['junctionNum']
		junction = Junction.objects.get(number = junctionNum)
		if junction.visitNum <= 3:
			junction.visitNum += 1
			junction.save()
			message = 'waiting for ' +str(4-junction.visitNum) + 'more devices!'
		
		for vehicleData in data['QInfo']:
			serializer = QiSerializer(data = vehicleData)
			if serializer.is_valid():
				serializer.save()
			else:
				return JSONResponse(serializer.errors, status = 400)

		if junction.visitNum >= 4:
			makePhase(junction)
			Qi.objects.all().delete()
			message = 'next phase has been set!'

		green = Junction.objects.get(number = junctionNum).green

		return JSONResponse({"message": message, "phase": green}, status = 201)
	
	else:
		return HttpResponse('<h1>Request is not a Post request!</h1>')

def index(request):

	return HttpResponse('<h1>This is the junction app!</h1>')


def makePhase(junction):

	Q = Qi.objects.filter(junctionNum = junction)
	Q = [Q.filter(i = 1), Q.filter(i = 2), Q.filter(i = 3), Q.filter(i = 4)]
	Qlen = [len(Q[0]), len(Q[1]), len(Q[2]), len(Q[3])]

	if junction.isFirstPhase:
		junction.green = Qlen.index(max(Qlen)) + 1

	else:
		green = junction.green
		tempList = [1, 2, 3, 4]
		tempList.remove(green)
		Qij = []
		for k in tempList:
			Qij += [len([i for i in Q[green-1] for j in Q[k-1] if i.macadd == j.macadd])]

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

	#preparing to call algo:
	
	Qlen = numpy.array(Qlen)
	Qar = numpy.insert((numpy.array([junction.Qab, junction.Qac, junction.Qad]))/float(Qlen[0]), 0, 0)
	Qbr = numpy.insert((numpy.array([junction.Qba, junction.Qbc, junction.Qbd]))/float(Qlen[1]), 1, 0)
	Qcr = numpy.insert((numpy.array([junction.Qca, junction.Qcb, junction.Qcd]))/float(Qlen[2]), 2, 0)
	Qdr = numpy.insert((numpy.array([junction.Qda, junction.Qdb, junction.Qdc]))/float(Qlen[3]), 3, 0)
	#call algo:
	junction.green = algo(Qlen[0], Qlen[1], Qlen[2], Qlen[3], Qar, Qbr, Qcr, Qdr)
	junction.save()
	return junction.green
	
#the main algorhithm: returns the number of the road which should have green light for the next phase
def algo(Qa,Qb,Qc,Qd,Qar,Qbr,Qcr,Qdr):
	
    def Pressure(Qa):  #assumed linear
        return (2*Qa+1)
    U=numpy.zeros((4,4,4))
    U[0][0]=[0,17,18,19]
    U[1][1]=[16,0,14,18]
    U[2][2]=[13,11,0,14]
    U[3][3]=[9,7,8,0]
    
    Pressure_Array=Pressure(numpy.array([Qa,Qb,Qc,Qd]))  
    
    W=numpy.zeros((4,4))
    #Preparing Weights
    W[0]=numpy.maximum(((Qa*numpy.array(Qar))/U[0][0]*[0,Pressure(Qa)-Pressure(Qb),Pressure(Qa)-Pressure(Qc),Pressure(Qa)-Pressure(Qd)]),[0,0,0,0])
    W[1]=numpy.maximum(((Qb*numpy.array(Qbr))/U[1][1]*[Pressure(Qb)-Pressure(Qa),0,Pressure(Qb)-Pressure(Qc),Pressure(Qb)-Pressure(Qd)]),[0,0,0,0])
    W[2]=numpy.maximum(((Qc*numpy.array(Qcr))/U[2][2]*[Pressure(Qc)-Pressure(Qa),Pressure(Qc)-Pressure(Qb),0,Pressure(Qc)-Pressure(Qd)]),[0,0,0,0])
    W[3]=numpy.maximum(((Qd*numpy.array(Qdr))/U[3][3]*[Pressure(Qd)-Pressure(Qa),Pressure(Qd)-Pressure(Qb),Pressure(Qc)-Pressure(Qd),0]),[0,0,0,0])
    
    for i in range(4):
        W[i][i]=0
    b=0
    for i in range (4):
        a=numpy.sum(W*U[i])
        if(numpy.sum(W*U[i])>a):
            b=i
            
    return i+1

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
