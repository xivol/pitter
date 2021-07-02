function getCookie(name) {
          let matches = document.cookie.match(new RegExp(
            "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
          ));
          return matches ? decodeURIComponent(matches[1]) : undefined;
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

function getHtmlSearchResult(user_id, user_info) {
    return `
        <button class="list-group-item list-group-item-action" id="${user_id}">
            <strong>@${user_info.username}</strong><br/>${user_info.name}
        </button>
    `
}

function getHtmlSearchProfile(user_data){
    return `
    <div class="modal" tabindex="-1" role="dialog" id="profileModal" >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">@${user_data.username } profile</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body card">
            <div class="card-body">
                <div class="image mb-2"><img class="rounded-circle" width="150" src="http://127.0.0.1:8000/post/get-image?image_id=${user_data.profile_image ? user_data.profile_image : ''}&is_profile=true" alt=""></div>
                <div class="h5">${user_data.first_name} ${user_data.last_name}</div>
                <div>
                    <span class="h7 text-muted">@${user_data.username }</span>
                    <button class="btn btn-primary btn-sm ml-3 follow-button" id="${user_data.username }" type="button">Follow</button>
                </div>
                <div class="h7">${user_data.description}</div>
            </div>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <div class="h6 text-muted">Followers</div>
                    <div class="h5" id="followers_num">${user_data.num_of_followers}</div>
                </li>
                <li class="list-group-item">
                    <div class="h6 text-muted">Following</div>
                    <div class="h5">${user_data.num_of_subscriptions}</div>
                </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    `
}


$(document).ready(function() {
    // Search bar logic
    // split for myHeaders1/2 is temp
    // error was that request with same united myHeaders don't work too
    // so I split them in separate ones. This doesn't work too
    let myHeaders1 = new Headers();
    let myHeaders2 = new Headers();
    myHeaders1.append("X-CSRF-TOKEN", getCookie("csrf_access_token"));
    myHeaders2.append("X-CSRF-TOKEN", getCookie("csrf_access_token"));
    $("#search-user" ).keydown(function() {
    // console.log( this.value );
    const url = backendBaseURL + '/user/search-user?user_info=' + this.value
    getData(url)
        .then((data) => {
            if (data.status === 200) {
                data.json()
                    .then((users) => {
                        // console.log(Object.keys(users).length)
                        let search_results = ""
                        let search_layout = $('.search-layout')
                        if (Object.keys(users).length > 0){
                            for (const [user_id, user_info] of Object.entries(users)) {
                              search_results+=(getHtmlSearchResult(user_id, user_info))
                            }
                            // console.log(search_results)
                        }
                        search_layout.html(search_results);
                    })
            }
        })
        .catch((e) => console.log(e));
    });

    // Modal with user info and follow button
    $('.search-layout').on('click', '.list-group-item', function(e) {
        let user_id = $(this).attr('id')
        // console.log(user_id)
        const url = backendBaseURL + '/user/user-info-id?id=' + user_id
        getData(url)
            .then((data) => {
                if (data.status === 200) {
                    data.json()
                        .then((user_data) => {
                            // console.log(user_data)
                            let modal_results = ""
                            let modal_layout = $('.modal-layout')
                            if (Object.keys(user_data).length > 0){
                                modal_results+=(getHtmlSearchProfile(user_data))
                                // console.log(search_results)
                            }
                            // console.log(modal_results)
                            modal_layout.html(modal_results);
                            $('#profileModal').modal('show');
                        })
                }
            })
            .catch((e) => console.log(e));


    });

    // follow button action
    $('.modal-layout').on('click', '.follow-button', function(e){
        // myHeaders.append("X-CSRF-TOKEN", getCookie("csrf_access_token"));
        let username = $(this).attr('id')
        let followers = parseInt($("#followers_num").text(),10);
        if($(this).hasClass('btn-primary')){
            $(this).toggleClass('btn-outline-danger');
            $(this).toggleClass('btn-primary');
            const url = backendBaseURL + '/follower/set-follower?username=' + username
            postDataImage(url, myHeaders1)
                .then((data) => {
                    // console.log(data.status)
                    if (data.status === 200) {
                        $("#followers_num").html(followers + 1)
                         $(this).text('Followed');
                    }})
        } else {
            $(this).toggleClass('btn-outline-danger');
            $(this).toggleClass('btn-primary');
            const url = backendBaseURL + '/follower/delete-follower?username=' + username
            postDataImage(url, myHeaders2)
                .then((data) => {
                    // console.log(data.status)
                    if (data.status === 200) {
                        $("#followers_num").html(followers - 1)
                        $(this).text('Follow');
                    }
                })
        }
    });
});

