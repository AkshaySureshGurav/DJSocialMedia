from django.contrib import admin
from .models import User, Posts, likesDislikes, follower
# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
admin.site.register(likesDislikes)
admin.site.register(follower)

