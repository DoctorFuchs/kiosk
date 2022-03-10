(async () => {
    await fetch("storage/edit_box.html")
        .then(res => res.text())
        .then(data => edit_box = data)

    await fetch("storage/create_box.html")
        .then(res => res.text())
        .then(data => create_box = data)

    await fetch("storage/header_bar.html")
        .then(res => res.text())
        .then(data => bar = data)

    do {
        if (document.readyState == "complete") {
            loadItems();
        }
    } while (!document.readyState == "complete");
})()

document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("submit", () => { setTimeout(loadItems, 1000) });
    // temporarily fix for the issue that items can refresh before request was send with slow servers
})

var req_args = "?sort=%sort%&revert=%revert%"
var _by = ""
var _revert = "false"

function order(by) {
    if (by == _by) {
        _revert = _revert == "false" ? "true" : "false";
    }
    else {
        _by = by
        _revert = false
    }
    loadItems()
}

function get_order() {
    return req_args.replaceAll("%sort%", _by).replaceAll("%revert%", _revert)
}

function edit(itemnumber) {
    var item = document.getElementById("item_" + String(itemnumber));
    var itemname = item.childNodes[0].textContent;
    var itemcost = item.childNodes[1].textContent.replace("€", "");
    var itemamount = item.childNodes[2].textContent;
    overlay_on(edit_box
        .replaceAll("%itemname%", itemname.trim())
        .replaceAll("%itemcost%", itemcost.trim())
        .replaceAll("%itemamount%", itemamount.trim()))
    loadItems()
}

function loadItems() {
    function items_callback(response) {
        let item = document.getElementById("item-table");
        let req = reformat(response);
        item.innerHTML = ""
        item.innerHTML += bar
        for (let i = 0; i < req.length; i++) {
            let req_ = req[i].split(",")
            req_[0] = req_[0].replaceAll("'", "").replaceAll("+", " ")
            req_[1] = req_[1].replaceAll("'", "")
            req_[2] = req_[2].replaceAll("'", "")
            item.innerHTML += "<tr class='item' id='item_" + i + "' onclick='edit(" + i + ")'><td class='left'>" + req_[0] + "</td><td>" + req_[1] + "€</td><td class='right'>" + req_[2] + "</td></tr>"
        }
    }
    request("/shop/list" + get_order(), callback = items_callback)
}

function create() {
    overlay_on(create_box)
}

function exitForm() {
    overlay_off();
    loadItems()
}

function deleteitem(itemname) {
    request("/shop/delete?item_name=" + itemname);
    overlay_off()
    loadItems()
}
