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

utc = pytz.UTC
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
	''' Create new user. while creating the user send only the required parameters.
	update user profile. access to admin for destroying the user. '''
	queryset = User.objects.all()
	serializer_class = UserSerializer

	def get_permissions(self):
		permission_classes = []
		if self.action == 'create':
			permission_classes = [AllowAny]
		elif self.action == 'retrieve':
			permission_classes = [AllowAny]
		elif self.action == 'update' or self.action == 'partial_update':
			permission_classes = [IsLoggedInUserOrAdmin]
		elif self.action == 'list' or self.action == 'destroy':
			permission_classes = [IsAdminUser]
		return [permission() for permission in permission_classes]

	def create(self, request, *args, **kwargs):
		try:
			response_data = super(UserViewSet, self).create(request, *args, **kwargs)
			data = response_data.data
			return Response(data, status.HTTP_201_CREATED)
		except Exception as e:
			try:
				print(e)
				exception = e.__dict__
				if exception.get('detail', {}).get('username', None):
					return Response({"error": "user with this username already exists."},status.HTTP_422_UNPROCESSABLE_ENTITY)

				other_errors = exception.get('detail', {}).get('non_field_errors', None)
				if other_errors:
					error_messages = ""
					for other_error in other_errors:
						error_messages += str(other_error)
					return Response({"error": error_messages}, status.HTTP_422_UNPROCESSABLE_ENTITY)

				other_errors = exception.get('detail', {}).get('contact_number', None)
				if other_errors:
					error_messages = ""
					for other_error in other_errors:
						error_messages += str(other_error) + " "
					return Response({"error": error_messages}, status.HTTP_422_UNPROCESSABLE_ENTITY)

				return Response({"error": "Please check your email or contact number username"},status.HTTP_422_UNPROCESSABLE_ENTITY)
			except Exception as e:
				return Response({"error": "Something Went wrong"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

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
            otp_verification = OTPVerification.objects.get_or_create(otp_to=otp_to, otp_type='email')[0]
            otp_verification.send_otp()
            return Response({"message": "OTP is sent to your Email", "otp_verification_id": otp_verification.id}, status.HTTP_200_OK)
        else:
            return Response({"error": "Please Enter Email or contact number"}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class VerifyOTP(APIView):
    """End point To Verify the OTP. Send (contact_number and country_code[country_code: srt]) or email and otp in parameters"""
    permission_classes = [AllowAny]


    def create_user_name(self, full_name):
        user_name = full_name.split()[0] + str(random.randint(100,9999))
        users = User.objects.filter(username = user_name)
        if users:
            user_name = self.create_user_name(full_name)
        return user_name

    def create_referral_code(self):
        N = 9
        referral_code = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
        users = User.objects.filter(referral_code = referral_code)
        if users:
            referral_code = self.create_referral_code()
        return referral_code

    def post(self, request):
        contact_number = request.data.get("contact_number", None)
        phone_code = request.data.get("phone_code", None)
        email = request.data.get("email", None)
        otp = request.data.get("otp", None)
        otp_verification_id = request.data.get("otp_verification_id", None)
        full_name = request.data.get("full_name", None)
        referral_code = request.data.get("referral_code", None)

        
        if not email and not contact_number and not phone_code:
            return Response({"error": "Please Enter Email or contact number and Phone code"},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not otp:
            return Response({"error": "Please Enter OTP"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not otp_verification_id:
            return Response({"error": "Please Enter OTP Verification ID"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if full_name is None:
            if contact_number:
                user = User.objects.filter(contact_number = contact_number)
                if user:
                    pass
                # else:
                #     return Response({"error": "Please create user first"},
                #             status.HTTP_422_UNPROCESSABLE_ENTITY)
        otp_verification = OTPVerification.objects.get(pk=otp_verification_id)

        otp_to = ""

        if contact_number and phone_code:
            otp_to = f"{phone_code}{contact_number}"
        elif email:
            otp_to = email

        if not otp_verification.validate_otp(otp_to, otp):
            return Response({"error": "Invalid OTP"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        # user = None
        if contact_number and phone_code:
            user = User.objects.filter(contact_number=contact_number, phone_code=phone_code).first()
        elif email:
            user = User.objects.filter(email=email).first()

        if not user:
            if full_name is None:
                return Response({"error": "Please provide full_name for signup."},
                            status.HTTP_422_UNPROCESSABLE_ENTITY)
            else:
                username = self.create_user_name(full_name)
                if contact_number and phone_code:
                    # username = f"dummyinvun@{phone_code}{contact_number}"
                    user = User.objects.create(full_name = full_name, username=username, contact_number=contact_number, phone_code=phone_code)
                elif email:
                    # username = f"dummyinvun@{email}"
                    user = User.objects.create(full_name = full_name, username=username, email=email)
                user.coin = 100
                user.referral_code = self.create_referral_code()
                if referral_code is not None:
                    referr = User.objects.filter(referral_code = referral_code)
                    referred = user
                    if referr:
                        referr = referr.last()
                        user_referral = UserReferral.objects.create(referr = referr, referred = user)
                        referr.coin = int(referr.coin) + 1000
                        referred.coin = int(referred.coin) + 500
                        referr.save()

        if user:
            if email:
                if not user.email_verified:
                    user.email_verified = True
                    user.save()

            if contact_number:
                if not user.contact_number_verified:
                    user.contact_number_verified = True
                    user.save()
            res = user.get_tokens_for_user()
            user_serializer = UserSimpleSerializer(user, many=False)
            return Response({"token": res['access'], "user": user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Something went wrong"}, status.HTTP_422_UNPROCESSABLE_ENTITY)



