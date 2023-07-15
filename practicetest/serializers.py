from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from content.serializers import UploadContentSerializer
from practicetest.models import *
from user.models import User

class PracticeTestSerializer(ModelSerializer):
	""" User Basic Information Serializer """
	content = serializers.SerializerMethodField()
	is_bookmarked = serializers.SerializerMethodField()
	is_challanged = serializers.SerializerMethodField()

	class Meta:
		model = PracticeTest
		fields = ('id','test_type','question_type','question','option','answer','content','created_at','updated_at', 'is_bookmarked', 'is_challanged')

	def get_content(self, obj):
		return UploadContentSerializer(obj.content).data

	def get_is_bookmarked(self, obj):
		user_id = self.context['user_id']
		user_practice = UserPractice.objects.filter(user__id = user_id, practice_test = obj)
		if user_practice:
			return user_practice.last().is_bookmarked

	def get_is_challanged(self, obj):
		user_id = self.context['user_id']
		user_practice = UserPractice.objects.filter(user__id = user_id, practice_test = obj)
		if user_practice:
			return user_practice.last().is_challanged