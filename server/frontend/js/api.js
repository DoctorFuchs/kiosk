function decode(jsonData) {
    if (Array.isArray(jsonData)) {
        jsonData = jsonData.map(item => {
            return decode(item)
        })
    }
    else if (typeof jsonData == "object") {
        entries = Object.entries(jsonData)
        jsonData = {}
        entries.forEach(entrie => {
            jsonData[entrie[0]] = decode(entrie[1])
        });
        console.dir(jsonData)
    } else {
        jsonData = encodeURIComponent(jsonData)
    }
    return jsonData
}

function request(path, callback_func = console.log, shouldDecode = true) {
    // make a request to a path of the api. It's a shortcut for json responses. (for example from /api/shop/list)
    let response = fetch("/api" + path)

    if (shouldDecode) {
        response
            .then(resp => { return resp.json() })
            .then(resp => { return decode(resp) })
            .then(resp => { callback_func(resp) })
    }
}
