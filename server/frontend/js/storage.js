initialize()

// this is a function because this code has to be run asyncronously
async function initialize() {
    // get templates
    edit_box = await loadTemplate("storage/edit_box.html");
    create_box = await loadTemplate("storage/create_box.html");
    bar = await loadTemplate("storage/header_bar.html");
    item_template = await loadTemplate("storage/item_template.html");

    // load items when DOMContent is loaded
    if (document.readyState == "loading") {
        document.addEventListener("DOMContentLoaded", loadItems)
    } else {
        loadItems()
    }
    // close form on submit
    document.addEventListener("submit", exitForm)
}

function edit(itemname) {
    /* create an edit_box from template.
     * Gets template informations from item_name argument*/

    // get informations about the item => resp object contains values of an item_model
    request("/shop/item?item_name=" + itemname, resp => {
        // create editbox overlay
        overlay_on(edit_box
            .replaceAll("%itemname%", decodeURIComponent(resp["name"]))
            .replaceAll("%itemname_encoded%", resp["name"])
            .replaceAll("%itemcost%", resp["cost"])
            .replaceAll("%itemamount%", resp["amount"])
        );
    });
}

// update items and render them into the list
function loadItems() {
    // get item table to render
    var item_table = document.getElementById("items");

    // clear list
    item_table.innerHTML = ""

    // render header bar from template
    item_table.innerHTML += bar

    var select_element = document.getElementById("sort_by");
    let arguments = String(select_element.options[select_element.selectedIndex].getAttribute("name")).split(";");
    let _key = arguments[0];
    let _reverse = arguments[1] == "true";

    request("/shop/list", response => {

        response.sort((a, b) => {
            var item_a, item_b;
            if (_key == "name") {
                // ignore lower/uppercase
                item_a = a[_key].toUpperCase();
                item_b = b[_key].toUpperCase();
            }
            else {
                item_a = parseFloat(a[_key]);
                item_b = parseFloat(b[_key]);
            }
            if (item_a > item_b) {
                return _reverse ? -1 : 1;
            }
            else if (item_b > item_a) {
                return _reverse ? 1 : -1;
            }
            else {
                return 0;
            }
        })

        // if list is empty skip render and return
        if (response.lenght === 0) {
            return;
        }

        // render for each item a template => item_template
        var table_items = ""
        response.forEach(item => {
            var elem = document.createElement("div");
            elem.innerHTML += item_template
                .replaceAll("/item_name/", decodeURIComponent(item["name"]))
                .replaceAll("/item_name_encoded/", item["name"])
                .replaceAll("/item_cost/", item["cost"])
                .replaceAll("/item_amount/", item["amount"]);

            if (item["amount"] <= 0) {
                elem.children[0].classList.add("w3-border");
                elem.children[0].classList.add("w3-border-red");
                elem.children[0].classList.add("w3-red");
            }
            table_items += elem.innerHTML;
        })
        item_table.innerHTML += table_items
    })
}

function create() {
    // create box to create new items
    overlay_on(create_box);
}

function exitForm() {
    // quit any form
    overlay_off();
}

async function deleteitem(item_name) {
    // delete item item_name
    exitForm();
    await fetch("/api/shop/delete?item_name=" + item_name, {
        "method": "DELETE"
    });
    loadItems()
}

function waitForReload() {
    document.getElementById("hiddeniframe").addEventListener("load", loadItems)
}
