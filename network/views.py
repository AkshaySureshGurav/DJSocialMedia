from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Posts, likesDislikes, follower
from django import forms

import datetime
import json

class postForm(forms.Form):
    messageOfUser = forms.CharField(max_length=1000, required=True, label='')

def index(request, pageNum=1):
    # print(type(request.user.id), request.user.id)
    allPosts = Posts.objects.all().order_by('-id')
    # print("number of pages - " + str(p.num_pages))
    # print(allP        osts)

    posts= None
    if allPosts.count() > 0:
        p = Paginator(allPosts, 10)
        if pageNum <= p.num_pages:
            posts = p.page(pageNum)
            # postsRelated = []
            for post in posts:
                likesDislikes = post.getLikeCount()
                
                likes = likesDislikes.filter(likes=True, dislikes=False).count()
                dislikes = likesDislikes.count() - likes
                post.likesCountForDOM = likes
                post.dislikesCountForDOM = dislikes

                if request.user.id: 
                    postWhereUserActioned = likesDislikes.filter(user=request.user)
                    if postWhereUserActioned:
                        if postWhereUserActioned.first().likes:
                            # if the user has liked the post in past then we use should disable the like button
                            post.ShouldDisLikeButtonDisabledDOM = False
                            post.ShouldLikeButtonDisabledDOM = True
                        else:
                            # if the user has disliked the post in past then we use should disable the dislike button
                            post.ShouldDisLikeButtonDisabledDOM = True
                            post.ShouldLikeButtonDisabledDOM = False
                    else:
                        post.ShouldDisLikeButtonDisabledDOM = False
                        post.ShouldLikeButtonDisabledDOM = False
                else:
                    post.ShouldDisLikeButtonDisabledDOM = True
                    post.ShouldLikeButtonDisabledDOM = True    
                # print(likes, dislikes)
                # postsRelated.append(p)
                # print(post.getLikeCount())
                # print()

            return render(request, "network/index.html", {
                "viewer": request.user if request.user.id else None,
                "form": postForm if request.user.id else None,
                "posts": posts,
                "currentPage": pageNum,
                "havePreviousPage": posts.has_previous(),
                "haveNextPage": posts.has_next()
            })
        
    return render(request, "network/index.html", {
        "viewer": request.user,
        "form": postForm, 
        "posts": posts,
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def newPost(request):
    # print("In newPost")
    if request.method == "POST":
        #
        # print(formData)
        requestBody = json.loads(request.body)
        # if len(requestBody["message"])
        if len(requestBody["message"]) < 1:
            return JsonResponse(
                {
                    "status": "notOK", 
                    "message": "Request didn't process successfully"
                }
            )
        # print(request.user)
        newPost = Posts(message=requestBody["message"], poster=request.user)
        
        newPost.save()
        # print(newPost.timestamp)
        return JsonResponse(
            {
                "status": "OK", 
                "message": "Request was processed successfully",
                "newPost": {
                    "id": int(newPost.id),
                    "message": str(newPost.message),
                    "timestamp": str(newPost.timestamp),
                    "poster": str(newPost.poster.username),
                    "posterID": newPost.poster.id
                }
            }
        )
    else:
        requestData = json.loads(request.body)
        # print(requestData)
        post = Posts.objects.get(id=requestData["postID"])
        post.message = requestData["newUserMessage"]
        post.timestamp = datetime.datetime.now().strftime('%a %d %b %Y, %I:%M%p')
        post.save()
        return JsonResponse(
            {
                "status": "OK", 
                "message": "Request was processed successfully",
                "responseData": {
                    "newTimeStamp": post.timestamp 
                }
            }
        )



@login_required
def profile(request, userId, pagenumber=1):
    # print(type(userId))
    isViewerTheCreatorOfProfile = request.user.id == userId
    # print(isViewerTheCreatorOfProfile)
    # user is the person of which we are viewing the profile
    creator = User.objects.get(id=userId)
    # print(creator)
    userPosts = Posts.objects.filter(poster=creator).order_by("-id")

    if isViewerTheCreatorOfProfile:
        countOfFollowers = follower.objects.filter(user=request.user).count()
        countOfFollowing = follower.objects.filter(follower=request.user).count()

        if userPosts.count() > 0:
            p = Paginator(userPosts, 10)
            if pagenumber <= p.num_pages:
                posts = p.page(pagenumber)
                # print(posts.count())
                # print(posts.object_list)
                for post in posts:
                    # print(post)
                    likesDislikes = post.getLikeCount()
                    
                    likes = likesDislikes.filter(likes=True, dislikes=False).count()
                    dislikes = likesDislikes.count() - likes
                    post.likesCountForDOM = likes
                    post.dislikesCountForDOM = dislikes

                    if request.user.id: 
                        postWhereUserActioned = likesDislikes.filter(user=request.user)
                        if postWhereUserActioned:
                            if postWhereUserActioned.first().likes:
                                # if the user has liked the post in past then we use should disable the like button
                                post.ShouldDisLikeButtonDisabledDOM = False
                                post.ShouldLikeButtonDisabledDOM = True
                            else:
                                # if the user has disliked the post in past then we use should disable the dislike button
                                post.ShouldDisLikeButtonDisabledDOM = True
                                post.ShouldLikeButtonDisabledDOM = False
                        else:
                            post.ShouldDisLikeButtonDisabledDOM = False
                            post.ShouldLikeButtonDisabledDOM = False
                    else:
                        post.ShouldDisLikeButtonDisabledDOM = True
                        post.ShouldLikeButtonDisabledDOM = True    
                    # print(likes, dislikes)
                    # postsRelated.append(p)
                    # print(post.getLikeCount())
                    # print()

                return render(request, "network/profilePage.html", {
                    "page": "profilePage",
                    "symbol": creator.username[0], 
                    "username": creator.username,
                    "creatorID": creator.id,
                    "countOfFollowers": countOfFollowers,
                    "countOfFollowing": countOfFollowing,
                    "showFollowButton": False,
                    "viewer": request.user if request.user.id else None,
                    "posts": posts,
                    "currentPage": pagenumber,
                    "havePreviousPage": posts.has_previous(),
                    "haveNextPage": posts.has_next()
                })
        else:
            return render(request, "network/profilePage.html", {
                "page": "profilePage",
                "symbol": creator.username[0], 
                "creatorID": creator.id,
                "username": creator.username,
                "countOfFollowers": countOfFollowers,
                "countOfFollowing": countOfFollowing,
                "showFollowButton": False,
                "posts": None
            })
    else:
        # print(follower.objects.filter(user=request.user))
        countOfFollowing = follower.objects.filter(follower=creator).count()
        countOfFollowers = follower.objects.filter(user=creator).count()
        isviewerFollowing = follower.objects.filter(user=creator, follower=request.user).exists()

        # user = User.objects.get(id=userId)
        if userPosts.count() > 0:
            p = Paginator(userPosts, 10)
            if pagenumber <= p.num_pages:
                posts = p.page(pagenumber)
                # print(posts.count())
                # print(posts.object_list)
                for post in posts:
                    # print(post)
                    likesDislikes = post.getLikeCount()
                    
                    likes = likesDislikes.filter(likes=True, dislikes=False).count()
                    dislikes = likesDislikes.count() - likes
                    post.likesCountForDOM = likes
                    post.dislikesCountForDOM = dislikes

                    if request.user.id: 
                        postWhereUserActioned = likesDislikes.filter(user=request.user)
                        if postWhereUserActioned:
                            if postWhereUserActioned.first().likes:
                                # if the user has liked the post in past then we use should disable the like button
                                post.ShouldDisLikeButtonDisabledDOM = False
                                post.ShouldLikeButtonDisabledDOM = True
                            else:
                                # if the user has disliked the post in past then we use should disable the dislike button
                                post.ShouldDisLikeButtonDisabledDOM = True
                                post.ShouldLikeButtonDisabledDOM = False
                        else:
                            post.ShouldDisLikeButtonDisabledDOM = False
                            post.ShouldLikeButtonDisabledDOM = False
                    else:
                        post.ShouldDisLikeButtonDisabledDOM = True
                        post.ShouldLikeButtonDisabledDOM = True    
                    # print(likes, dislikes)
                    # postsRelated.append(p)
                    # print(post.getLikeCount())
                    # print()

                return render(request, "network/profilePage.html", {
                    "page": "profilePage",
                    "symbol": creator.username[0], 
                    "username": creator.username,
                    "creatorID": creator.id,
                    "viewerID": request.user.id,
                    "countOfFollowers": countOfFollowers,
                    "countOfFollowing": countOfFollowing,
                    "showFollowButton": True,
                    "FollowingBtnValue": "Unfollow" if isviewerFollowing else "Follow",
                    "viewer": request.user if request.user.id else None,
                    "posts": posts,
                    "currentPage": pagenumber,
                    "havePreviousPage": posts.has_previous(),
                    "haveNextPage": posts.has_next()
                })
        else:
            return render(request, "network/profilePage.html", {
                "page": "profilePage",
                "symbol": creator.username[0], 
                "username": creator.username,
                "creatorID": creator.id,
                "viewerID": request.user.id,
                "countOfFollowers": countOfFollowers,
                "countOfFollowing": countOfFollowing,
                "showFollowButton": True,
                "FollowingBtnValue": "Unfollow" if isviewerFollowing else "Follow",
                "posts": None
            })
        
    
# only takes put request
def changeFollowingStatus(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        requester = User.objects.get(id=int(data["requester"]))
        creator = User.objects.get(id=int(data["creator"]))

        # print("Request from " + requester.username + " to " + data["action"] + " " + creator.username)


        if data["action"] == "Follow":
            addFollower = follower(user=creator, follower=requester)
            addFollower.save()
        else: 
            try:
                removeFollower = follower.objects.filter(user=creator, follower=requester)
                # print(removeFollower)
                removeFollower.first().delete()
                removeFollower.save()
            except:
                print("User does not follow creater, so can't delete")
            # print(removeFollower)

        # so the user will be on the creators page now so we also have to update the followers count

        updatedFollowers = follower.objects.filter(user=creator).count()
        updatedFollowing = follower.objects.filter(follower=creator).count()

        return JsonResponse(
            {
                "status": "OK", 
                "message": "Request was processed successfully", 
                "data": {
                    "updatedFollowers": updatedFollowers,
                    "updatedFollowing": updatedFollowing
                }
            }
        )
    else:
        return JsonResponse(
            {
                "status": "notOK", 
                "message": "Request was not accepted"
            })
    

def following(request, pageNumber=1):
    # getting the list of the creators the user follow
    creator_array = follower.objects.filter(follower=request.user)
    # print(creator_array)
    creators = []
    for creator in creator_array:
        creators.append(creator.user)
    # got the creators array now 

    postsFromCreator = Posts.objects.filter(poster__in=creators).order_by("-id")
    # print(postsFromCreator.count())
    posts= None
    if postsFromCreator.count() > 0:
        p = Paginator(postsFromCreator, 10)
        if pageNumber <= p.num_pages:
            posts = p.page(pageNumber)
            # print(posts.count())
            # print(posts.object_list)
            for post in posts:
                # print(post)
                likesDislikes = post.getLikeCount()
                
                likes = likesDislikes.filter(likes=True, dislikes=False).count()
                dislikes = likesDislikes.count() - likes
                post.likesCountForDOM = likes
                post.dislikesCountForDOM = dislikes

                if request.user.id: 
                    postWhereUserActioned = likesDislikes.filter(user=request.user)
                    if postWhereUserActioned:
                        if postWhereUserActioned.first().likes:
                            # if the user has liked the post in past then we use should disable the like button
                            post.ShouldDisLikeButtonDisabledDOM = False
                            post.ShouldLikeButtonDisabledDOM = True
                        else:
                            # if the user has disliked the post in past then we use should disable the dislike button
                            post.ShouldDisLikeButtonDisabledDOM = True
                            post.ShouldLikeButtonDisabledDOM = False
                    else:
                        post.ShouldDisLikeButtonDisabledDOM = False
                        post.ShouldLikeButtonDisabledDOM = False
                else:
                    post.ShouldDisLikeButtonDisabledDOM = True
                    post.ShouldLikeButtonDisabledDOM = True    
                # print(likes, dislikes)
                # postsRelated.append(p)
                # print(post.getLikeCount())
                # print()

            return render(request, "network/following.html", {
                "page": "following",
                "viewer": request.user if request.user.id else None,
                "posts": posts,
                "currentPage": pageNumber,
                "havePreviousPage": posts.has_previous(),
                "haveNextPage": posts.has_next()
            })
    else:
        return render(request, "network/following.html", {
            "page": "following",
            "posts": None
        })


def likeDislikePost(request):
    requestData = json.loads(request.body)
    # print(requestData)
    postLikesDislikes = likesDislikes.objects.filter(post=int(requestData["postID"]), user=request.user)
    # print(postLikesDislikes.first().likes, postLikesDislikes.first().dislikes)

    if postLikesDislikes.exists():
        post = postLikesDislikes.first()
        # print(post.getLikeCount())
        if requestData["action"] == "like":
            post.likes = True
            post.dislikes = False
        else:
            post.dislikes = True
            post.likes = False
        post.save()
    else:
        post = likesDislikes.objects.create(post=Posts.objects.get(id=int(requestData["postID"])), user=request.user)
        if requestData["action"] == "like":
            post.likes = True
        else:
            post.dislikes = True
        post.save()

    updatedPost = Posts.objects.get(id=int(requestData["postID"]))
    likesDislikesOfUpdatedPost = updatedPost.getLikeCount()
    
    likesOfUpdatedPost = likesDislikesOfUpdatedPost.filter(likes=True, dislikes=False).count()
    dislikesOfUpdatedPost = likesDislikesOfUpdatedPost.count() - likesOfUpdatedPost
        
    return JsonResponse(
        {
            "status": "OK",
            "updatedPost": {
                "id": int(requestData["postID"]),
                "likes": likesOfUpdatedPost,
                "dislikes": dislikesOfUpdatedPost
            }
        }
    )