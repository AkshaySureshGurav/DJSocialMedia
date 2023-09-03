
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pageNum>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("profile/<int:userId>", views.profile, name="profile"),
    path("profile/<int:userId>/page/<int:pagenumber>", views.profile, name="profile"),
    path("changeFollowingStatus", views.changeFollowingStatus, name="changeFollowingStatus"),
    path("following", views.following, name="following"),
    path("following/<int:pageNumber>", views.following, name="following"),
    path("likeDislikePost", views.likeDislikePost, name="likeDislikePost")
]
