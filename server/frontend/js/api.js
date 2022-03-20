function request(path, callback_func = console.log) {
    // make a request to a path of the api. It's a shortcut for json responses. (for example from /api/shop/list)
    fetch("/api" + path)
        .then(resp => { return resp.json() })
        .then(resp => { callback_func(resp) })
}
