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
	
	QabRat = models.FloatField(default = 0.33)
	QacRat = models.FloatField(default = 0.33)
	QadRat = models.FloatField(default = 0.33)
	QbaRat = models.FloatField(default = 0.33)
	QbcRat = models.FloatField(default = 0.33)
	QbdRat = models.FloatField(default = 0.33)
	QcaRat = models.FloatField(default = 0.33)
	QcbRat = models.FloatField(default = 0.33)
	QcdRat = models.FloatField(default = 0.33)
	QdaRat = models.FloatField(default = 0.33)
	QdbRat = models.FloatField(default = 0.33)
	QdcRat = models.FloatField(default = 0.33)

	visitNum = models.IntegerField(default = 0)

	def __unicode__(self):
		return str(self.number)

class Qi(models.Model):
	junctionNum = models.ForeignKey(Junction, on_delete = models.CASCADE)
	i = models.IntegerField()
	macadd = models.CharField(max_length = 20)