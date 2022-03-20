// get templates
var edit_box = loadTemplate("storage/edit_box.html");
var create_box = loadTemplate("storage/create_box.html");
var bar = loadTemplate("storage/header_bar.html");
var item_template = loadTemplate("storage/item_template.html");


function edit(itemname) {
    /* create an edit_box from template. 
     * Gets template informations from item_name argument*/

    // get informations about the item => resp object contains values of an item_model
    request("/shop/item?item_name=" + itemname, resp => {
        // create editbox overlay
        edit_box.then(template => {
            overlay_on(template
                .replaceAll("%itemname%", resp["name"])
                .replaceAll("%itemcost%", resp["cost"])
                .replaceAll("%itemamount%", resp["amount"])
            );
        })
    });
    // load items to make changes visible
    loadItems();
}

function loadItems() {
    // update items and render them into the list

    request("/shop/list", response => {
        // get item table to render 
        var item_table = document.getElementById("items");

        // render header bar from template
        bar.then(template => { item_table.innerHTML += template });

        // if list is empty skip render and return
        if (response.lenght === 0) { return; }

        // clear list
        item_table.innerHTML = "";

        // render for each item a template => item_template
        response.forEach(item => {
            item_template.then(template => {
                item_table.innerHTML += template
                    .replaceAll("/item_name/", item["name"])
                    .replaceAll("/item_cost/", item["cost"])
                    .replaceAll("/item_amount/", item["amount"]);
            }
            )
        })
    })
}

function create() {
    // create box to create new items
    create_box.then(box => { overlay_on(box); });
}

function exitForm() {
    // default exit form and update by making overlay hidden and update items
    overlay_off();
    loadItems();
}

function deleteitem(item_name) {
    // delete item from item_name
    fetch("/shop/delete/" + item_name, {
        "method": "DELETE"
    });
    exitForm();
}

// load items when DOMContent is loaded
document.addEventListener("DOMContentLoaded", loadItems())
// close form on submit
document.addEventListener("submit", e => {
    exitForm();
})