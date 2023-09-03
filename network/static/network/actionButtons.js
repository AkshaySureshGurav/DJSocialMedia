document.addEventListener("DOMContentLoaded", () => {
    console.log("Adding the eventListeners")
    document.querySelectorAll("button[class^='actionButton']").forEach(btn => {
        btn.addEventListener("click", (e) => clickedActionBtn(e))
    })

    const clickedActionBtn= (e) => {
        console.log("Clicked")
        // alert(`User clicked on btn ${e.currentTarget.value}`)

        const [action, postID] = e.currentTarget.value.split('/');

        switch(action) {
            case "share": 
                share()
                break;
            case "like":
                like(postID)
                break;
            case "dislike":
                dislike(postID)
                break;
            case "edit":
                edit(postID)
                break;
            default: 
                console.log("No action was provided")
                break;
        }
    }

    function share() {
        alert('This functionality if currently unavailable');
    }

    function getCsrfToken(formID) {
        const form = document.querySelector(`#${formID}`);
        if (form) {
            const csrfTokenInput = form.querySelector("input[name='csrfmiddlewaretoken']");
            if (csrfTokenInput) {
                return csrfTokenInput.value;
            }
        }
        return null; // Return null if the form or CSRF token is not found
    }
    

    function like(postID) {
        console.log('User like the post ' + postID);
        const token = getCsrfToken("actionButtonsForm")
        fetch("/likeDislikePost", {
            method: "POST",
            headers: {
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                "postID": postID,
                "action": "like"
            })
        })
        .then(response => {
            if (!response.ok) {
                // console.error("Response not OK")
                alert("Like was not counted because of internal server issue")
                throw new Error("Error happened while connecting or from server side");
            }
            return response.json()
        }).then(data => {
            const post = document.querySelector(`#post${data.updatedPost.id}`)
            post.querySelector(".likesCountForDOM").innerText = data.updatedPost.likes;
            post.querySelector(".dislikesCountForDOM").innerText = data.updatedPost.dislikes;
            post.querySelector(".like").disabled = true
            post.querySelector(".dislike").disabled = false
        })
        .catch(err => {
            console.error(err)
        })
    }

    function dislike(postID) {
        console.log('User disliked the post ' + postID);
        const token = getCsrfToken("actionButtonsForm")
        fetch("/likeDislikePost", {
            method: "POST",
            headers: {
                "X-CSRFToken": token
            },
            body: JSON.stringify({
                "postID": postID,
                "action": "dislike"
            })
        })
        .then(response => {
            if (!response.ok) {
                // console.error("Response not OK")
                alert("Dislike was not counted because of internal server issue")
                throw new Error("Error happened while connecting or from server side");
            }
            return response.json()
        }).then(data => {
            console.log("reached here")
            const post = document.querySelector(`#post${data.updatedPost.id}`)
            post.querySelector(".likesCountForDOM").innerText = data.updatedPost.likes;
            post.querySelector(".dislikesCountForDOM").innerText = data.updatedPost.dislikes
            post.querySelector(".like").disabled = false
            post.querySelector(".dislike").disabled = true
        })
        .catch(err => {
            console.error(err)
        })
    }

    function edit(postID) {
        console.log("in edit function for post " + postID)
        const post = document.getElementById(`post${postID}`);
        const postActionsHolder = post.querySelector("#postAction");
        const postMessage = post.querySelector(".postMessage");
        const updateMessageFormSubmit = post.querySelector("#newMessageSubmit");
        const updateMessageForm = post.querySelector("#updateMessageForm");

        postActionsHolder.style.display = "none";
        postMessage.style.display = "none";
        updateMessageForm.style.display = "block";
        
        updateMessageFormSubmit.addEventListener("click", () => {
            const csrfToken = getCsrfToken("udpatePostFormCSRFHolder")
            const newUserMessage = post.querySelector("#newMessageOfUser").value;
            fetch("/newPost", {
                method: "PUT",
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    "postID": postID,
                    "newUserMessage": newUserMessage
                })
            })
            .then(response => {
                if (!response.ok) {
                    // console.error("Response not OK")
                    alert("Post was not updated")
                    throw new Error("Error happened while connecting or from server side");
                }
                return response.json()
            }).then(data => {
                postMessage.innerText = newUserMessage;
                post.querySelector(".postTimeStamp").innerText = data.responseData.newTimeStamp;
                postMessage.style.display = "block";
                updateMessageForm.style.display = "none";
                postActionsHolder.style.display = "block";
            })
            .catch(err => {
                console.error(err)
            })
        })
    }
})