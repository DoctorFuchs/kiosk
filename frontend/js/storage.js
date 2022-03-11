var edit_box;
var create_box;
var bar;
var item_template;

// load templates
fetch("storage/edit_box.html")
    .then(res => res.text())
    .then(data => edit_box = data)

fetch("storage/create_box.html")
    .then(res => res.text())
    .then(data => create_box = data)

fetch("storage/header_bar.html")
    .then(res => res.text())
    .then(data => bar = data)

fetch("storage/item_template.html")
    .then(res => res.text())
    .then(data => item_template = data)



var req_args = "?sort=%sort%&revert=%revert%"
var _by = ""
var _revert = "false"

function order(by) {
    if (by==_by) {
        _revert = _revert=="false"?"true":"false";
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

function edit(itemname) {
    request("/shop/item?item_name=" + itemname, resp => {
        overlay_on(edit_box
            .replaceAll("%itemname%", resp["name"])
            .replaceAll("%itemcost%", resp["cost"])
            .replaceAll("%itemamount%", resp["amount"]));
    });
    loadItems()
}

function loadItems() {
    function items_callback(response) {
        var item_table = document.getElementById("items");
        item_table.innerHTML = "";
        item_table.innerHTML += bar;
        response.forEach(item => {
            item_table.innerHTML += item_template.replaceAll("/item_name/", item["name"]).replaceAll("/item_cost/", item["cost"]).replaceAll("/item_amount/", item["amount"]);
        })
    }
    request("/shop/list"+get_order(), callback=items_callback)
}

function create() {
    overlay_on(create_box)
}

function exitForm() {
    overlay_off();
    loadItems()
}

function deleteitem(itemname) {
    request("/shop/delete?item_name="+itemname);
    overlay_off()
    loadItems()
}

document.addEventListener("DOMContentLoaded", loadItems())
document.addEventListener("submit", loadItems())