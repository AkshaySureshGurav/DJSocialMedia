document.addEventListener("DOMContentLoaded", () => {
    try {
        const newPostForm = document.querySelector("#newPostForm");
        newPostForm.addEventListener("submit", (e) => {
            e.preventDefault()
            const csrfToken = getCsrfToken("newPostForm")
            const userMessage = newPostForm.querySelector("input[name='messageOfUser']").value
            
            if (userMessage.length < 1) {
                alert("The message cannot be empty")
            }

            fetch("/newPost", {
                method: "POST",
                headers: {
                    // 'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken, // Add the CSRF token to the request headers
                },
                body: JSON.stringify({
                    "message": userMessage
                })
            })
            .then(response => {
                if (!response.ok) {
                    console.error("Response not OK")
                    throw new Error("Error happened while connecting or from server side");
                }
                return response.json()
            })
            .then(data => {
                console.log(data)
                const post = document.createElement("section")
                post.className = "post"
                post.id = `post${data.newPost.id}`
                post.innerHTML = `
                    <section class="postHeader">
                        <a class="inlineChild" href="{% url 'profile' userId=${data.newPost.posterID} %}">
                            <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000">
                                <g><rect fill="none" height="24" width="24"/>
                                </g><g><g>
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM7.35 18.5C8.66 17.56 10.26 17 12 17s3.34.56 4.65 1.5c-1.31.94-2.91 1.5-4.65 1.5s-3.34-.56-4.65-1.5zm10.79-1.38C16.45 15.8 14.32 15 12 15s-4.45.8-6.14 2.12C4.7 15.73 4 13.95 4 12c0-4.42 3.58-8 8-8s8 3.58 8 8c0 1.95-.7 3.73-1.86 5.12z"/>
                                <path d="M12 6c-1.93 0-3.5 1.57-3.5 3.5S10.07 13 12 13s3.5-1.57 3.5-3.5S13.93 6 12 6zm0 5c-.83 0-1.5-.67-1.5-1.5S11.17 8 12 8s1.5.67 1.5 1.5S12.83 11 12 11z"/>
                                </g></g>
                            </svg>
                            <p class="postPoster">${data.newPost.poster}</p>
                        </a>
                        <p class="postTimeStamp">${data.newPost.timestamp}</p>
                    </section>
                    <section class="postContent">
                        <p class="postMessage">${data.newPost.message}</p>
                    </section>
                    <section id="updateMessageForm" style="display: none;">
                        <input type="text" name="newMessageOfUser" id="newMessageOfUser">
                        <input type="submit" id="newMessageSubmit" value="update"></input>
                    </section>
                    <section id="postAction" class="inlineChild" style="float: right;">
                        <section class="inlineChild">
                            <button class="actionButton like" value="like/${data.newPost.id}">
                                <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0zm0 0h24v24H0V0z" fill="none"/><path d="M9 21h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.58 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2zM9 9l4.34-4.34L12 10h9v2l-3 7H9V9zM1 9h4v12H1z"/></svg>
                            </button>
                            <p class="likesCountForDOM">0</p>
                        </section>
                        <section class="inlineChild" >
                            <button class="actionButton dislike" value="dislike/${data.newPost.id}"> 
                                <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0zm0 0h24v24H0V0z" fill="none"/><path d="M15 3H6c-.83 0-1.54.5-1.84 1.22l-3.02 7.05c-.09.23-.14.47-.14.73v2c0 1.1.9 2 2 2h6.31l-.95 4.57-.03.32c0 .41.17.79.44 1.06L9.83 23l6.59-6.59c.36-.36.58-.86.58-1.41V5c0-1.1-.9-2-2-2zm0 12-4.34 4.34L12 14H3v-2l3-7h9v10zm4-12h4v12h-4z"/></svg>
                            </button>
                            <p class="dislikesCountForDOM">0</p>
                        </section>
                        <section style="margin-right: 1vw;">
                            <button class="actionButton" value="share/unavailable">
                                <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92zM18 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM6 13c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm12 7.02c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/></svg> 
                            </button>
                        </section>
                        <section>
                            <button class="actionButton edit" value="edit/${data.newPost.id}">
                                <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M14.06 9.02l.92.92L5.92 19H5v-.92l9.06-9.06M17.66 3c-.25 0-.51.1-.7.29l-1.83 1.83 3.75 3.75 1.83-1.83c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.2-.2-.45-.29-.71-.29zm-3.6 3.19L3 17.25V21h3.75L17.81 9.94l-3.75-3.75z"/></svg>                   
                            </button>
                        </section>
                    </section>     
                `
                const postsHolder = document.getElementById("postsHolder")
                const firstChild = postsHolder.firstChild;
                postsHolder.insertBefore(post, firstChild)
                newPost = postsHolder.firstElementChild
                let actionButtons = ['like', "dislike", "share", "edit"];
                actionButtons.forEach(actionType => {
                    newPost.querySelector(`.${actionType}`).addEventListener("click", (e) => clickedActionBtn(e))
                })
            })
            .catch(error => {
                console.log(error)
            })
        })
    } catch(err) {
        console.log(err)
    }

    // document.querySelectorAll("button").forEach(btn => {
    //     btn.addEventListener("click", (e) => clickedActionBtn(e))
    // })

    // const clickedActionBtn= (e) => {
    //     // alert(`User clicked on btn ${e.currentTarget.value}`)

    //     const [action, postID] = e.currentTarget.value.split('/');

    //     switch(action) {
    //         case "share": 
    //             share()
    //             break;
    //         case "like":
    //             like(postID)
    //             break;
    //         case "dislike":
    //             dislike(postID)
    //             break;
    //         case "edit":
    //             edit(postID)
    //             break;
    //         default: 
    //             console.log("No action was provided")
    //             break;
    //     }
    // }

    // function share() {
    //     alert('This functionality if currently unavailable');
    // }

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
    

    // function like(postID) {
    //     console.log('User like the post ' + postID);
    //     const token = getCsrfToken("actionButtonsForm")
    //     fetch("/likeDislikePost", {
    //         method: "POST",
    //         headers: {
    //             "X-CSRFToken": token
    //         },
    //         body: JSON.stringify({
    //             "postID": postID,
    //             "action": "like"
    //         })
    //     })
    //     .then(response => {
    //         if (!response.ok) {
    //             // console.error("Response not OK")
    //             alert("Like was not counted because of internal server issue")
    //             throw new Error("Error happened while connecting or from server side");
    //         }
    //         return response.json()
    //     }).then(data => {
    //         const post = document.querySelector(`#post${data.updatedPost.id}`)
    //         post.querySelector(".likesCountForDOM").innerText = data.updatedPost.likes;
    //         post.querySelector(".dislikesCountForDOM").innerText = data.updatedPost.dislikes;
    //         post.querySelector(".like").disabled = true
    //         post.querySelector(".dislike").disabled = false
    //     })
    //     .catch(err => {
    //         console.error(err)
    //     })
    // }

    // function dislike(postID) {
    //     console.log('User disliked the post ' + postID);
    //     const token = getCsrfToken("actionButtonsForm")
    //     fetch("/likeDislikePost", {
    //         method: "POST",
    //         headers: {
    //             "X-CSRFToken": token
    //         },
    //         body: JSON.stringify({
    //             "postID": postID,
    //             "action": "dislike"
    //         })
    //     })
    //     .then(response => {
    //         if (!response.ok) {
    //             // console.error("Response not OK")
    //             alert("Dislike was not counted because of internal server issue")
    //             throw new Error("Error happened while connecting or from server side");
    //         }
    //         return response.json()
    //     }).then(data => {
    //         console.log("reached here")
    //         const post = document.querySelector(`#post${data.updatedPost.id}`)
    //         post.querySelector(".likesCountForDOM").innerText = data.updatedPost.likes;
    //         post.querySelector(".dislikesCountForDOM").innerText = data.updatedPost.dislikes
    //         post.querySelector(".like").disabled = false
    //         post.querySelector(".dislike").disabled = true
    //     })
    //     .catch(err => {
    //         console.error(err)
    //     })
    // }

    // function edit(postID) {
    //     console.log("in edit function for post " + postID)
    //     const post = document.getElementById(`post${postID}`);
    //     const postActionsHolder = post.querySelector("#postAction");
    //     const postMessage = post.querySelector(".postMessage");
    //     const updateMessageFormSubmit = post.querySelector("#newMessageSubmit");
    //     const updateMessageForm = post.querySelector("#updateMessageForm");

    //     postActionsHolder.style.display = "none";
    //     postMessage.style.display = "none";
    //     updateMessageForm.style.display = "block";
        
    //     updateMessageFormSubmit.addEventListener("click", () => {
    //         const csrfToken = getCsrfToken("udpatePostFormCSRFHolder")
    //         const newUserMessage = post.querySelector("#newMessageOfUser").value;
    //         fetch("/newPost", {
    //             method: "PUT",
    //             headers: {
    //                 'X-CSRFToken': csrfToken
    //             },
    //             body: JSON.stringify({
    //                 "postID": postID,
    //                 "newUserMessage": newUserMessage
    //             })
    //         })
    //         .then(response => {
    //             if (!response.ok) {
    //                 // console.error("Response not OK")
    //                 alert("Post was not updated")
    //                 throw new Error("Error happened while connecting or from server side");
    //             }
    //             return response.json()
    //         }).then(data => {
    //             postMessage.innerText = newUserMessage;
    //             post.querySelector(".postTimeStamp").innerText = data.responseData.newTimeStamp;
    //             postMessage.style.display = "block";
    //             updateMessageForm.style.display = "none";
    //             postActionsHolder.style.display = "block";
    //         })
    //         .catch(err => {
    //             console.error(err)
    //         })
    //     })
    // }

})

