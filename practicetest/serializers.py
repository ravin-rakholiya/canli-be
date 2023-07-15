from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from content.serializers import UploadContentSerializer
from practicetest.models import *

class PracticeTestSerializer(ModelSerializer):
	""" User Basic Information Serializer """
	content = serializers.SerializerMethodField()

	class Meta:
		model = PracticeTest
		fields = ('id','test_type','question_type','question','option','answer','content','created_at','updated_at')

	def get_content(self, obj):
		return UploadContentSerializer(obj.content).data