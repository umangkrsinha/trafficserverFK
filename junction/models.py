# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Junction(models.Model):
	number = models.IntegerField(primary_key=True)
	
	QaNum = models.IntegerField(default = 0)
	QbNum = models.IntegerField(default = 0)
	QcNum = models.IntegerField(default = 0)
	QdNum = models.IntegerField(default = 0)
	
	Qab = models.FloatField(default = 10)
	Qac = models.FloatField(default = 10)
	Qad = models.FloatField(default = 10)
	Qba = models.FloatField(default = 10)
	Qbc = models.FloatField(default = 10)
	Qbd = models.FloatField(default = 10)
	Qca = models.FloatField(default = 10)
	Qcb = models.FloatField(default = 10)
	Qcd = models.FloatField(default = 10)
	Qda = models.FloatField(default = 10)
	Qdb = models.FloatField(default = 10)
	Qdc = models.FloatField(default = 10)

	visitNum = models.IntegerField(default = 0)

	green = models.IntegerField(default = 1)

	isFirstPhase = models.BooleanField(default = True)

	def __unicode__(self):
		return str(self.number)

class Qi(models.Model):
	junctionNum = models.ForeignKey(Junction, on_delete = models.CASCADE)
	i = models.IntegerField()
	macadd = models.CharField(max_length = 20)