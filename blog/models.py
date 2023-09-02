from django.db import models
from  django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    post_no = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="")
    heading1 = models.CharField(max_length=100, default="")
    content1 = models.TextField()
    heading2 = models.CharField(max_length=100, default="")
    content2 = models.TextField()
    heading3 = models.CharField(max_length=100, default="")
    content3 = models.TextField()
    slug = models.CharField(max_length=100, default="")
    views = models.IntegerField(default=0)
    author = models.CharField(max_length=50, default="")
    publishing_time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + ' by ' + self.author

class BlogComment(models.Model):
    s_no = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:14] + "... " + "by " + self.user.username