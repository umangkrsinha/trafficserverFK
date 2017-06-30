from django.db import models
from .models import Qi, Junction
#from .models import DeviceData
from rest_framework import serializers

#class DeviceDataSerializer(serializers.ModelSerializer):

#	class Meta:
#		model = DeviceData
#		fields = ('lon', 'lat', 'dev_id')

class JunctionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Junction
		fields = '__all__'

class QiSerializer(serializers.ModelSerializer):

	class Meta:
		model = Qi
		fields = '__all__'
