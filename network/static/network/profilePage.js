document.addEventListener("DOMContentLoaded", () => {
    const followUnfollowForm = document.getElementById("followUnfollowBtn");

    followUnfollowForm.addEventListener("submit", (event) => {
        event.preventDefault()
        // console.log(`Clicked on submit button`)
        const csrfToken = followUnfollowForm.querySelector("input[name='csrfmiddlewaretoken']").value
        const hiddenValue = followUnfollowForm.querySelector("input[name='userIDs']")
        const [requester, creator, action] = hiddenValue.value.split('/');
        // console.log(requester, creator, action)

        const BTN = followUnfollowForm.querySelector("button")
        // console.log(BTN)
        // console.log(creator)
        fetch("/changeFollowingStatus", {
            method:"PUT",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, // Add the CSRF token to the request headers
            },
            body: JSON.stringify({
                "requester" : requester,
                "creator": creator, 
                "action": action
            })
        }).then(response => {
            if (!response.ok) {
                console.log("error occured")
            }
            return response.json()
        })
        .then(processedResponse => {
            if (processedResponse.status != "OK") {
                console.log("Internal server issue")
                return null
            }
            console.log("request was successfull");

            if (action == "Follow") {
                BTN.innerText = "Unfollow"
                hiddenValue.value = `${requester}/${creator}/Unfollow`
            } else {
                BTN.innerText = "Follow"
                hiddenValue.value = `${requester}/${creator}/Follow`
            }
            document.getElementById("followersCount").innerText = `Followers: ${processedResponse.data.updatedFollowers} / Following: ${processedResponse.data.updatedFollowing}`
            
        }).catch(error => console.error())
    })
})