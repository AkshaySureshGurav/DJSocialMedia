from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass


class Posts(models.Model):
    message = models.TextField(max_length=1000)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.CharField(default=datetime.datetime.now().strftime('%a %d %b %Y, %I:%M%p'), max_length=50)
    # the below for field's value comes handy only while sending the context to render html 
    # and some part of html is rendered based on this four values
    likesCountForDOM = models.IntegerField(default=0)
    dislikesCountForDOM = models.IntegerField(default=0)
    ShouldLikeButtonDisabledDOM = models.BooleanField(default=False)
    ShouldDisLikeButtonDisabledDOM = models.BooleanField(default=False)

    def getLikeCount(self):
        return self.likesCount.all()

    def __str__(self) -> str:
        return self.message + " by " + self.poster.username + " on " + str(self.timestamp)


class likesDislikes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="likesCount")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likedPosts", null=True)
    likes = models.BooleanField(default=False)
    dislikes = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.post.message + " -> " + self.user.username 


class follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Followers")
    # following = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.follower.username + " follows " + self.user.username 
