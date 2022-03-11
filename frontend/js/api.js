function request(path, callback_func=console.log) {
    fetch("/api" + path)
        .then(resp => { return resp.json() })
        .then(resp => { callback_func(resp) })
}


