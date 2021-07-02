const backendBaseURL = "http://127.0.0.1:5000"


async function refreshToken() {
    console.log('Try refresh');
    let myHeaders = new Headers();
    myHeaders.append("X-CSRF-TOKEN", getCookie("csrf_refresh_token"));
    for (let head of myHeaders.entries())
        console.log(head);
    const resp = await fetch(backendBaseURL+'/refresh', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        credentials: 'include', // include, *same-origin, omit
        headers: myHeaders,
    })
        .then((data) => {
            console.log('Token is refreshed')
            if (data.status !== 200)
                logout()
        })
        .catch((e) => console.log(e));
    console.log(resp)
    return resp
}

function getCookie(name) {
          let matches = document.cookie.match(new RegExp(
            "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
          ));
          return matches ? decodeURIComponent(matches[1]) : undefined;
}

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function validateSignUpForm() {
    function isCorrectField(element, condition) {
        if (!condition) {
            element.addClass("wrongValue");
            return false;
        }
        else if (element.is('.wrongValue'))
            element.removeClass('wrongValue')

        return true;
    }

    const username = $("input[id=username-up]")
    const email = $("input[id=email-up]");
    const last_name = $("input[id=surname-up]");
    const password = $("input[id=password-up]");
    console.log(username)
    console.log(email)
    console.log(last_name)
    console.log(password)
    return (
        isCorrectField(username, username.val().length > 0)
        && isCorrectField(email, validateEmail(email.val()))
        && isCorrectField(last_name, last_name.val().length > 0)
        && isCorrectField(password, password.val().length > 5)
    )
}

async function postData(url = '', data = {}) {
    // Default options are marked with *
    return await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    }); // parses JSON response into native JavaScript objects
}


function signUpForm() {
    console.log(validateSignUpForm())
    if (!validateSignUpForm())
        return null

    const signUpBody = {
        "username":$("input[id=username-up]").val(),
        "email":$("input[id=email-up]").val(),
        "first_name":$("input[id=name-up]").val(),
        "last_name": $("input[id=surname-up]").val(),
        "description": $("input[id=description-up]").val(),
        "password": $("input[id=password-up]").val(),
    };

    console.log(signUpBody);
    const url = backendBaseURL + "/user/create-user";

    postData(url, signUpBody)
        .then((data) => {
            console.log("Got data", data); // JSON data parsed by `response.json()` call
            if (data.status === 200)
                window.location.reload(false)
        })
        .catch((e) => console.log(e));
}

function logInForm() {
    const logInBody = {
        "username":$("input[name=username]").val(),
        "password": $("input[name=password]").val(),
    };
    console.log(logInBody);
    const url = backendBaseURL + "/login";

    postData(url, logInBody)
        .then((data) => {
            if (data.status === 200)
                window.location.reload(false)
            console.log("Log In data", data); // JSON data parsed by `response.json()` call
        })
        .catch((e) => console.log(e));
}

async function logout() {
    fetch(backendBaseURL + "/logout", {
        method: 'DELETE', // *GET, POST, PUT, DELETE, etc.
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie("csrf_access_token")
        },
    }).then(response => {
        if (response.status === 200)
            window.location.reload(false)
        else if (response.status === 422)
            refreshToken().then((data) => {
                if (data.status === 200)
                    logout()
        })
        .catch((e) => console.log(e));
    })
    .catch((e) => console.log(e));

}
