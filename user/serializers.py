from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from user.models import *


class UserSerializer(ModelSerializer):
	"""" User Serializer for creating and updating the user """
	gender_detail = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'full_name', 'dob', 'gender', 'location_city','gender_detail', 'email_verified',  ]
		extra_kwargs = {'password': {'write_only': True}}

	def validate(self, attrs):
		email = attrs.get('email', None)

		if not self.instance:
			if not email:
				raise serializers.ValidationError("Contact number or Email should be present")

		if email:
			qs = User.objects.filter(email=email)
			if self.instance:
				qs = qs.exclude(id=self.instance.id)

			if qs.exists():
				raise serializers.ValidationError("User with this Email is already Exist")
		return attrs

		def validate_email(self, value):
			# write your validation for particular column
			return value

	def create(self, validated_data):
		password = "password"
		user = User(**validated_data)
		user.set_password("password")
		user.save()
		user.send_otp_to_user(action="SIGN_UP_MSG")
		return user

	def update(self, instance, validated_data):
		instance.email = validated_data.get('email', instance.email)
		instance.username = validated_data.get('email', instance.email)
		instance.full_name = validated_data.get('full_name', instance.full_name)
		instance.dob = validated_data.get('dob', instance.dob)
		instance.gender = validated_data.get('gender', instance.gender)
		instance.location_city = validated_data.get('location_city', instance.gender)
		instance.save()
		return instance

	def get_gender_detail(self, obj):
		get_gender = obj.gender
		if get_gender == 'M':
			return "Male"
		elif get_gender == 'F':
			return "Female"
		else:
			return None
