from django.db import models
from django.db import models
from user.models import User


def content_upload_path(instance, filename):
    return 'content/{0}/{1}/{2}'.format(
        instance.uploader.id,
        instance.type_of_content,
        filename
        )
# Create your models here.
class Content(models.Model):
    """ Content model for storing all types of contents """

    TYPE_OF_CONTENT = (
                            ("image", "Image"),
                           )

    uploader = models.ForeignKey("user.User", on_delete=models.CASCADE,
                             limit_choices_to={"is_active": True})
    type_of_content = models.CharField(max_length=10,
                                        choices=TYPE_OF_CONTENT,
                                        )
    content = models.FileField(upload_to=content_upload_path)
    extention = models.CharField(max_length=50, blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, null=True)
    offline_locator=models.CharField(max_length=20, blank=True, null=True)