from django.urls import path, include
from rest_framework import routers
from practicetest import views

urlpatterns = [
	path('fetch/questionbank', views.FetchQuestionAPIView.as_view(), name='generate-otp'),
	path('bookmark/question', views.BookmarkQuestionAPIView.as_view(), name='bookmark-question'),
	path('challange/question', views.ChallangeQuestionAPIView.as_view(), name='challange-question'),
	path('fetch/practice/test', views.FetchPracticeTestAPIView.as_view(), name='fetch-practice-test'),

]