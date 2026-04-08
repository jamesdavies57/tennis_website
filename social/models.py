from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    POST_TYPES = (
        ("NEWS", "News"),
        ("QUESTION", "Question"),
        ("DISCUSSION", "Discussion"),
        ("OTHER", "Other")
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    post_type = models.CharField(max_length=15, choices=POST_TYPES, default="OTHER")
    title = models.CharField(max_length = 50)
    body = models.CharField(max_length = 500)
    locked = models.BooleanField(default=False)
    upload_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    body = models.CharField(max_length = 500)
    upload_time = models.DateTimeField(default=timezone.now)