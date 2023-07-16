from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from practicetest.models import *
from django.db.models import Q
from practicetest.serializers import *

# Create your views here.
class FetchQuestionAPIView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_classes = []

	def get(self, request):
		try:
			user = request.user
			context = {"user_id": user.id}
			user_practices = UserPractice.objects.filter(user = user, is_bookmarked = True)
			question_type = request.query_params.get("question_type", None)
			questions = PracticeTest.objects.filter(question_type = question_type)
			return Response({"response":PracticeTestSerializer(questions, context = context, many = True).data}, status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({"error":"something went wrong"}, status.HTTP_400_BAD_REQUEST)

class BookmarkQuestionAPIView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_classes = []

	def post(self, request):
		try:
			practice_test_id = request.data.get("question_id", None)
			is_bookmark = request.data.get("bookmark", None)
			if practice_test_id:
				user = request.user
				questions = PracticeTest.objects.get(id=practice_test_id)
				user_practice = UserPractice.objects.filter(user = user, practice_test = questions)
				if user_practice:
					user_practice = user_practice.last()
					user_practice.is_bookmarked = is_bookmark
					user_practice.save()
				else:
					user_practice = UserPractice.objects.create(user = user, practice_test = questions, is_bookmarked = is_bookmark)
				return Response({"response":"Bookmarked Updated Successfully."}, status.HTTP_200_OK)
			else:
				return Response({"response":"please provide question id"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
		except Exception as e:
			print(e)
			return Response({"error":"something went wrong"}, status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		try:
			user = request.user
			context = {"user_id": user.id}
			user_practices = UserPractice.objects.filter(is_bookmarked = True, user = user)
			practice_test = []
			if user_practices:
				for user_practice in user_practices:
					if user_practice.practice_test.question_type != "note":
						practice_test.append(user_practice.practice_test)
			return Response({"response":PracticeTestSerializer(practice_test, context = context, many = True).data}, status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({"error":"something went wrong"}, status.HTTP_400_BAD_REQUEST)



class ChallangeQuestionAPIView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_classes = []

	def post(self, request):
		try:
			practice_test_id = request.data.get("question_id", None)
			is_challanged = request.data.get("is_challanged", None)
			if practice_test_id:
				user = request.user
				questions = PracticeTest.objects.get(id=practice_test_id)
				user_practice = UserPractice.objects.filter(user = user, practice_test = questions)
				if user_practice:
					user_practice = user_practice.last()
					user_practice.is_challanged = is_challanged
					user_practice.save()
				else:
					user_practice = UserPractice.objects.create(user = user, practice_test = questions, is_bookmarked = is_bookmark)
				return Response({"response":"Challanged Updated Successfully."}, status.HTTP_200_OK)
			else:
				return Response({"error":"please provide question id"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
		except Exception as e:
			print(e)
			return Response({"error":"something went wrong"}, status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		try:
			user = request.user
			context = {"user_id": user.id}
			user_practices = UserPractice.objects.filter(is_challanged = True, user = user)
			practice_test = []
			if user_practices:
				for user_practice in user_practices:
					if user_practice.practice_test.question_type != "note":
						practice_test.append(user_practice.practice_test)
			return Response({"response":PracticeTestSerializer(practice_test, context = context, many = True).data}, status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({"error":"something went wrong"}, status.HTTP_400_BAD_REQUEST)

class FetchStaredNotesAPIView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_classes = []

	def get(self, request):
		try:
			user = request.user
			context = {"user_id": user.id}
			user_practices = UserPractice.objects.filter(is_bookmarked = True, user = user)
			practice_test = []
			if user_practices:
				for user_practice in user_practices:
					if user_practice.practice_test.question_type == "note":
						practice_test.append(user_practice.practice_test)
			return Response({"response":PracticeTestSerializer(practice_test, context = context, many = True).data}, status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({"error":"something went wrong"}, status.HTTP_400_BAD_REQUEST)


class FetchPracticeTestAPIView(APIView):
	permission_classes = [IsAuthenticated]
	serializer_classes = []

	def get(self, request):
		try:
			user = request.user
			context = {"user_id": user.id}
			practice_test_id = request.query_params.get("practice_test_number", None)
			if practice_test_id is None:
				return Response({"error":"please provide practice test number"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
			sign_questions = PracticeTest.objects.filter(question_type = "sign").order_by('?')[:20]
			rule_questions = PracticeTest.objects.filter(question_type = "rule").order_by('?')[:20]
			return Response({"response":PracticeTestSerializer(sign_questions.union(rule_questions), context = context,many = True).data}, status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({"error":"something went wrong"}, status.HTTP_400_BAD_REQUEST)



