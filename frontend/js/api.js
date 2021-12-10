function callback(str) {
    console.log(str)
}

function getAPIport() {
    return API
}

function request(path, callback_func=callback) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            callback_func(decodeURI(xhr.response));
        }
    }

    xhr.open('GET', "http://localhost:"+String(getAPIport())+path, true);
    xhr.send(null);
}

function reformat(s) {
    if (s == "[]") {
        return []
    }
    return String(s).replace("]]", "").replace("[[", "").split("], [");
}

