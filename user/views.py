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
    # Add this code block
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
                exception = e.__dict__
                if exception.get('detail', {}).get('username', None):
                    return Response({"error": "user with this username already exists."},
                                    status.HTTP_422_UNPROCESSABLE_ENTITY)

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

class GenerateOTPV2(APIView):
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


class OTPVerification(models.Model):
    CHEAT_OTP = ["123456", "001100", "000111"]
    OTP_TYPE = (
        ('email', 'Email'),
    )

    otp_type = models.CharField(max_length=20,
                                choices=OTP_TYPE, blank=True, null=True)
    otp_to = models.CharField(max_length=50)
    otp = models.IntegerField(blank=True, null=True, )
    otp_validity = models.DateTimeField(blank=True, null=True, )

    def send_otp(self):
        expiry_time = datetime.now() + timedelta(minutes=10)
        otp = random.randrange(99999, 999999, 12)
        self.otp = otp
        self.otp_validity = expiry_time
        self.save()

        if self.otp_type == "email":
            send_email_verify_otp(otp, [self.otp_to])
        return True

    def validate_otp(self, otp_to, otp):
        valid = (self.otp == int(otp) and self.otp_validity >= utc.localize(datetime.now())) and self.otp_to == otp_to
        if settings.SYS_ENV != 'PROD' and not valid:
            if otp in self.CHEAT_OTP:
                valid = True
        if valid:
            self.delete()
        return valid
