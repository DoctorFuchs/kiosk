function decode(jsonData) {
    if (Array.isArray(jsonData)) {
        jsonData.forEach(item => {
            item = decode(item)
        })
        return jsonData
    }
    else if (typeof jsonData == "string") {
        return decodeURIComponent(jsonData)
    }
    else {
        Object.values(jsonData).forEach(item => {
            item = decode(item)
        })
        return jsonData
    }
}

function request(path, callback_func = console.log) {
    // make a request to a path of the api. It's a shortcut for json responses. (for example from /api/shop/list)
    fetch("/api" + path)
        .then(resp => { return resp.json() })
        .then(resp => { return decode(resp) })
        .then(resp => { callback_func(resp) })
}
