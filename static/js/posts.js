$( document ).ready(function() {
    getFeed();
    // Update token every 25 minutes.
    let intervalId = setInterval(refreshToken, 25*60*1000);
});

async function getData(url = '') {
    // Default options are marked with *
    return await fetch(url, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        credentials: 'include', // include, *same-origin, omit
    }); // parses JSON response into native JavaScript objects
}

async function postDataImage(url, headers = new Headers(), bodyData = new FormData()) {
    let requestOptions = {
        method: 'POST',
        headers: headers,
        body: bodyData,
        redirect: 'follow',
        credentials: 'include',
    };

    return await fetch(url, requestOptions)
}

function addPostRequest(myHeaders, postFormData) {
    postDataImage(backendBaseURL + "/post/create-post", myHeaders, JSON.stringify(postFormData))
                    .then(response => {
                        if (response.status === 200)
                            response.json()
                                .then(post => {
                                let posts_layout = $('.posts-layout')
                                console.log(posts_layout)
                                post.image_id
                                    ? posts_layout.prepend(getHtmlImagePost(post))
                                    : posts_layout.prepend(getHtmlPost(post))
                            })
                    })
                .catch(error => console.log('error', error));
}


function addPost(){
    const parentDiv = $('.tab-content');
    const activeDiv = parentDiv.children('.active');
    const text = activeDiv.find('.custom-text-input');
    const image = activeDiv.find('.custom-file-input');

    let myHeaders = new Headers();
    myHeaders.append("X-CSRF-TOKEN", getCookie("csrf_access_token"));

    let postFormData = {
        "content": text.val(),
        "visibility": $('.visibility-list').attr('id'),
    };

    if (image.get(0) && image.get(0).files[0]) {
        console.log('image');
        let formData = new FormData();
        formData.append("image", image.get(0).files[0]);

        postDataImage(backendBaseURL + "/post/upload-image", myHeaders, formData)
            .then(response => response.json())
            .then(imageID => {
                console.log(imageID);
                postFormData.image_id = imageID;
                addPostRequest(myHeaders, postFormData)
            })
            .catch(error => console.log('error', error));
    }
    else {
        addPostRequest(myHeaders, postFormData)
    }
    // postDataImage(backendBaseURL + "/post/create-post", myHeaders, JSON.stringify(postFormData))
    //                 .then(response => {
    //                     if (response.status === 200)
    //                         response.json()
    //                             .then(post => {
    //                             let posts_layout = $('.feed-layout')
    //                             console.log(posts_layout)
    //                             post.image_id
    //                                 ? posts_layout.prepend(getHtmlImagePost(post))
    //                                 : posts_layout.prepend(getHtmlPost(post))
    //                         })
    //                 })
    //             .catch(error => console.log('error', error));
}

function deletePost(delElem) {
    const mainPostDiv =$(delElem).closest('.main-post-div');
    console.log(mainPostDiv)
    const url = backendBaseURL + '/post/delete-post?post_id=' + mainPostDiv.attr('id')
    fetch(url, {
        method: 'DELETE', // *GET, POST, PUT, DELETE, etc.
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie("csrf_access_token")
        },
    }).then(response => {
        if (response.status === 200)
            mainPostDiv.remove()
        else if (response.status === 422)
            refreshToken()
                .then((data) => {
                    if (data.status === 200)
                        deletePost(delElem);
        })
    }).catch()
}
//
// post is result of response
function getHtmlPost(post_data) {
    return `
             <div class="card gedf-card main-post-div" id="${post_data.id}">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="mr-2">
                                    <img class="rounded-circle" width="45" src="http://127.0.0.1:8000/post/get-image?image_id=${post_data.profile_image_id ? post_data.profile_image_id : ''}&is_profile=true" alt="">
                                </div>
                                <div class="ml-2">
                                    <div class="h5 m-0">${post_data.first_name + ' ' + post_data.last_name}</div>
                                    <div class="h7 text-muted" id="${post_data.user_id}">@${post_data.username}</div>
                                    </div>
                                </div>
                                ${post_data.editable || post_data.removable ?
                                    `<div>
                                        <div class="dropdown">
                                            <button class="btn btn-link dropdown-toggle" type="button" id="gedf-drop1"
                                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <i class="fa fa-ellipsis-h"></i>
                                            </button>
                                                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="gedf-drop1">
                                                ${post_data.editable ?
                                                    `<a class="dropdown-item" href="#"><i class="fa fa-edit mr-2"></i>Edit</a>`
                                                    : ''
                                                }
                                                ${ post_data.removable ?
                                                    `<a class="dropdown-item btn-outline-danger" onclick="deletePost(this)"><i class="fa fa-trash mr-2"></i>Delete</a>`
                                                    : ''
                                                }
                                                </div>
                                            
                                        </div>
                                    </div>`
                                    : ''
                                }
                            </div>
                        </div>

                        <div class="card-body">
                            <div class="text-muted h7 mb-2">
                                <a class="card-link" href="#">
                                <i class="fa fa-clock-o"></i> ${post_data.time_from_now}${post_data.edited ? ' (edited)' : ''}
                                </a>
                            </div>
                            <p class="card-text">
                               ${post_data.content}
                            </p>
                        </div>
                        <div class="card-footer">
                            <button class="btn btn-primary card-link" onclick="changeLike(this)"><i class="fa fa-star"></i> ${post_data.likes} Like</button>
                            <!--<a href="#" class="card-link"><i class="fa fa-comment"></i> Comment</a>
                                <a href="#" class="card-link"><i class="fa fa-mail-forward"></i> Share</a> -->
                        </div>
                    </div>
             </div>
`
}

function getHtmlImagePost(post_data) {
    return `
             <div class="card gedf-card main-post-div" id="${post_data.id}">
                    <div class="card-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="mr-2">
                                    <img class="rounded-circle" width="45" src="http://127.0.0.1:8000/post/get-image?image_id=${post_data.profile_image_id}&is_profile=true" alt="">
                                </div>
                                <div class="ml-2">
                                    <div class="h5 m-0">${post_data.first_name + ' ' + post_data.last_name}</div>
                                    <div class="h7 text-muted" id="${post_data.user_id}">@${post_data.username}</div>
                                    </div>
                                </div>
                                ${post_data.editable || post_data.removable ?
                                    `<div>
                                        <div class="dropdown">
                                            <button class="btn btn-link dropdown-toggle" type="button" id="gedf-drop1"
                                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <i class="fa fa-ellipsis-h"></i>
                                            </button>
                                                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="gedf-drop1">
                                                ${post_data.editable ?
                                                    `<a class="dropdown-item" href="#"><i class="fa fa-edit mr-2"></i>Edit</a>`
                                                    : ''
                                                }
                                                ${ post_data.removable ?
                                                    `<a class="dropdown-item btn-outline-danger" onclick="deletePost(this)"><i class="fa fa-trash mr-2"></i>Delete</a>`
                                                    : ''
                                                }
                                                </div>
                                            
                                        </div>
                                    </div>`
                                    : ''
                                }
                            </div>
                        </div>

                        <div class="card-body">
                            <div class="text-muted h7 mb-2">
                                <a class="card-link" href="#">
                                <i class="fa fa-clock-o"></i> ${post_data.time_from_now}${post_data.edited ? ' (edited)' : ''}
                                </a>
                            </div>
                            <img class="rounded float-left mr-3 post-image" src="http://127.0.0.1:8000/post/get-image?image_id=${post_data.image_id}"/>
                            <p class="card-text">
                               ${post_data.content}
                            </p>
                        </div>
                        <div class="card-footer">
                            <button class="btn btn-primary card-link" onclick="changeLike(this)"><i class="fa fa-star"></i> ${post_data.likes} Like</button>
                            <!--<a href="#" class="card-link"><i class="fa fa-comment"></i> Comment</a>
                                <a href="#" class="card-link"><i class="fa fa-mail-forward"></i> Share</a> -->
                        </div>
                    </div>
             </div>
`
}

function getFeed() {
    const url = backendBaseURL + '/post/get-feed'

    getData(url, {})
        .then((data) => {
            if (data.status === 200) {
                data.json()
                    .then((posts) => {
                        if (posts.length > 0) {
                            posts.forEach((post) => {
                                let posts_layout = $('.posts-layout')
                                post.image_id
                                    ? posts_layout.append(getHtmlImagePost(post))
                                    : posts_layout.append(getHtmlPost(post))
                            })
                        }
                        else {
                            $('.posts-layout').append('Create your first post!')
                        }
                    })
            }
        })
        .catch((e) => console.log(e));
}

function changeLike(likeElem) {
    const mainPostDiv =$(likeElem).closest('.main-post-div');
    const url = backendBaseURL + '/post/change-likes?post_id=' + mainPostDiv.attr('id')
    getData(url).then((data) => {
        data.json().then((numOfLikes) => {
            $(likeElem).html('<i class="fa fa-star"></i> ' + numOfLikes + ' Like');
        })
    })
}

function changeVisibilityId(newId, iconClass) {
    console.log(newId, iconClass)
    if (['public', 'friends', 'personal'].includes(newId)) {
        $('.visibility-list').attr("id", newId);

        let visibilityIcon = $('.visibility-icon');
        visibilityIcon.removeClass('fa-globe');
        visibilityIcon.removeClass('fa-users');
        visibilityIcon.removeClass('fa-user');
        visibilityIcon.addClass(iconClass);
    }
}