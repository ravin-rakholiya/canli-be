from django.db import models
from user.models import User

# Create your models here.
class PracticeTest(models.Model):
    QUESTION_TYPE = (
        ('sign', 'Sign'),
        ('rule', 'Rule'),
    )
    TEST_TYPE = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    test_type = models.CharField(max_length=128, choices=TEST_TYPE, blank=True, null=True)
    question_type = models.CharField(max_length=128, choices=QUESTION_TYPE, blank=True, null=True)
    question = models.CharField(max_length=256, null = False, blank = False)
    option = models.CharField(max_length=256, null = False, blank = False)
    answer = models.CharField(max_length=128, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        ordering = ["-id"]

class UserPractice(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_practice_user')
	practice_test = models.ForeignKey(PracticeTest, on_delete=models.PROTECT, related_name='user_practice_test')
	is_challanged = models.BooleanField(default=False)
	is_bookmarked = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)

	def __str__(self):
		return f"{self.id}"

	class Meta:
		ordering = ["-id"]