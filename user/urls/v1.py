from django.urls import path, include
from rest_framework import routers
from user import views

urlpatterns = [
	path('generate_otp', views.GenerateOTP.as_view(), name='generate-otp'),
    path('verify_otp', views.VerifyOTP.as_view(), name='verify-otp'),
    path('edit/profile', views.EditProfile.as_view(), name='edit-profile'),
    path('add/feedback', views.UserFeedbackAPIView.as_view(), name='user-feedback'),
    path('add/test_date', views.AddTestDate.as_view(), name='add-testdate'),
]