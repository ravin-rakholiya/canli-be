from rest_framework.serializers import (ModelSerializer,)
from rest_framework import serializers
from user.models import *


class UserSimpleSerializer(ModelSerializer):
    """ User Basic Information Serializer """

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'dob', 'gender', 'location_city', 'email_verified',)

