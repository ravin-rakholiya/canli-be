import pytz
import random
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import ValidationError
from django.db import models
<<<<<<< HEAD
from rest_framework_simplejwt.tokens import RefreshToken
=======
>>>>>>> 9076a0f (created mail templated and SES for sending mail)
from notification.email_notifications import send_login_otp, send_signup_otp, send_report_user_notification, \
    send_email_verify_otp
# from notification.consts import OTP_MESSAGES
# from notification.email_notifications import send_login_otp, send_signup_otp, send_report_user_notification, \
#     send_email_verify_otp
# from notification.models import Notification

# from rest_framework_simplejwt.tokens import RefreshToken
# from math import sin, cos, sqrt, atan2, radians
# from ckeditor.fields import RichTextField

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=self.normalize_email(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    CHEAT_OTP = ['000000', '123456', '111111']
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    def save(self, *args, **kwargs):
        if self.pk == None:
            if not (self.email == None or self.email == ""):
                if User.objects.filter(email=self.email).exists():
                    return ValidationError("User Already Exist in  this mail id")

            if (self.username == None or self.username == ""):
                full_name = self.full_name
                if full_name:
                    username = "_".join(full_name.split(" "))
                    if User.objects.filter(username=username).exists():
                        self.username = self.email
                    else:
                        self.username = self.email

                email = self.email
                if email and not self.username:
                    mail_id = email.split("@")[0].lower()
                    if User.objects.filter(username=mail_id).exists():
                        uid = User.objects.last().id + 1
                        self.username = self.email
                    else:
                        self.username = self.email

            self.username = self.username.lower()
            if self.email:
                self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)


    username = models.CharField(max_length=255, unique=True, blank=False, null=False, )
    email = models.EmailField(blank=True, null=True, db_index=True)
    full_name = models.CharField(max_length=255, unique=False, blank=True, null=True, )
    dob = models.DateField(blank=True, null=True, )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    mobile_otp = models.IntegerField(blank=True, null=True, )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    location_city = models.CharField(max_length=40, null=True, blank=True)
    groups = models.ManyToManyField('auth.Group', blank=True, null=True, )
    test_date = models.DateField(blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = "username"

    # REQUIRED_FIELDS = ["email"]



    def has_perm(self, perm, obj=None):
        user_perms = []
        if self.is_staff:
            groups = self.groups.all()
            for group in groups:
                perms = [(f"{x.content_type.app_label}.{x.codename}") for x in group.permissions.all()]
                user_perms += perms

            if perm in user_perms:
                return True
        return (self.is_admin or self.is_superuser)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def send_otp_to_user(self, action="SIGN_UP_MSG"):
        expiry_time = datetime.now() + timedelta(minutes=10)
        otp = random.randrange(99999, 999999, 12)
        self.mobile_otp = otp
        self.mobile_otp_validity = expiry_time
        self.save()
        
        if self.email:
            if action == "SIGN_IN_MSG":
                send_login_otp(otp, [self.email])
            if action == "SIGN_UP_MSG":
                send_signup_otp(otp, [self.email])

            pass

        return True

    # def validate_otp(self, otp):
    #     valid = (self.mobile_otp == int(otp) and self.mobile_otp_validity >= utc.localize(datetime.now()))
    #     if True:  # settings.SYS_ENV != 'PROD' and not valid
    #         if otp in self.CHEAT_OTP:
    #             valid = True
    #     if valid:
    #         self.mobile_otp = None
    #         self.save()
    #     return valid

    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }



class OTPVerification(models.Model):
    CHEAT_OTP = ["123456", "001100", "000111"]
    otp_to = models.CharField(max_length=50)
    otp = models.IntegerField(blank=True, null=True, )
    otp_validity = models.DateTimeField(blank=True, null=True, )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        ordering = ["-id"]

    # def send_otp(self):
    #     expiry_time = datetime.now() + timedelta(minutes=10)
    #     otp = random.randrange(99999, 999999, 12)
    #     self.otp = otp
    #     self.otp_validity = expiry_time
    #     self.save()

    #     if self.otp_type == "mobile":
    #         OTP_SUFFIX = OTP_MESSAGES["OTP_SUFFIX"]
    #         OTP_PREFIX = OTP_MESSAGES["SIGN_UP_MSG"]
    #         message = OTP_MESSAGES["PASSCODE"] % {"otp": f"{self.otp}"}
    #         Notification.send_message(full_contact_number=self.otp_to, message=message)

    #     if self.otp_type == "email":
    #         send_email_verify_otp(otp, [self.otp_to])
    #     return True

    # def validate_otp(self, otp_to, otp):
    #     valid = (self.otp == int(otp) and self.otp_validity >= utc.localize(datetime.now())) and self.otp_to == otp_to
    #     if settings.SYS_ENV != 'PROD' and not valid:
    #         if otp in self.CHEAT_OTP:
    #             valid = True
    #     if valid:
    #         self.delete()
    #     return valid


class UserFeedback(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_feedback')
	feedback = models.TextField(null = False, blank = False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.id}"

	class Meta:
		ordering = ["-id"]