from rest_framework.serializers import (ModelSerializer,
                                        ValidationError,
                                        )
from rest_framework import serializers
from content.models import *
import io

class UploadContentSerializer(serializers.ModelSerializer):
	content_name = serializers.SerializerMethodField()

	class Meta:
		model = Content
		fields = ('id', 'type_of_content', 'content_name', 'content', 'extention', 'duration')

	def get_content_name(self, data):
		return data.content.name.split("/")[-1]