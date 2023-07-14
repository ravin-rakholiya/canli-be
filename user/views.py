from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import *
from user.permissions import *

utc = pytz.UTC
# Create your views here.
class EditProfile(APIView):
    permission_classes = [IsAuthenticated]
    serializer_classes = [UserSimpleSerializer]

    def post(self, request):
        user = request.user
        user.email = request.data.get('email', None)
        user.full_name = request.data.get('full_name', None)
        user.dob = request.data.get('dob', None)
        user.gender = request.data.get('gender', None)
        user.location_city = request.data.get('location_city', None)
        user.save()
        return Response({"response":"user profile updated successfully."}, status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        user_data = UserSimpleSerializer(user).data
        return Response({"response":user_data}, status.HTTP_200_OK)


class GenerateOTP(APIView):
    """End point To Generate/ReGenerate the OTP. Send contact_number and country_code [country_code:str] in parameters"""
    permission_classes = [AllowAny]

    def post(self, request):
        full_name = request.data.get("full_name", None)
        email = request.data.get("email", None)

        if not email:
            return Response({"error": "Please Enter Email"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if full_name is None:
            user = User.objects.filter(email = email)
            if user:
                pass
            else:
                return Response({"message": "Please make sign up."}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        elif email:
            otp_to = f"{email}"
            otp_verification = OTPVerification.objects.get_or_create(otp_to=otp_to)[0]
            otp_verification.send_otp()
            return Response({"message": "OTP is sent to your Email", "otp_verification_id": otp_verification.id}, status.HTTP_200_OK)
        else:
            return Response({"error": "Please Enter Email or contact number"}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class VerifyOTP(APIView):
    """End point To Verify the OTP. Send (contact_number and country_code[country_code: srt]) or email and otp in parameters"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", None)
        otp = request.data.get("otp", None)
        otp_verification_id = request.data.get("otp_verification_id", None)
        full_name = request.data.get("full_name", None)
        user = None
        
        if not email:
            return Response({"error": "Please Enter Email"},status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not otp:
            return Response({"error": "Please Enter OTP"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not otp_verification_id:
            return Response({"error": "Please Enter OTP Verification ID"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if full_name is None:
            if email:
                user = User.objects.filter(email = contact_number)
                if user:
                    pass
        otp_verification = OTPVerification.objects.get(pk=otp_verification_id)


        if not otp_verification.validate_otp(email, otp):
            return Response({"error": "Invalid OTP"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if user is None:
            if full_name is None:
                return Response({"error": "Please provide full_name for signup."},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                username = email
                user = User.objects.create(full_name = full_name, username=username, email=email)

        if user:
            if email:
                if not user.email_verified:
                    user.email_verified = True
                    user.save()
            res = user.get_tokens_for_user()
            user_serializer = UserSimpleSerializer(user, many=False)
            return Response({"token": res['access'], "user": user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Something went wrong"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

class UserFeedbackAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            feedback = request.data.get("feedback", None)
            if feedback is None or feedback == "":
                return Response({"error": "Please fill the feedback."}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            user_feedback = UserFeedback.objects.create(user = user, feedback = feedback)
            return Response({"response": "Feedback submitted successfully"}, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "something went wrong."}, status.HTTP_422_UNPROCESSABLE_ENTITY)

