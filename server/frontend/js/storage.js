var edit_box = loadTemplate("storage/edit_box.html");
var create_box = loadTemplate("storage/create_box.html");
var bar = loadTemplate("storage/header_bar.html");
var item_template = loadTemplate("storage/item_template.html");


function edit(itemname) {
    request("/shop/item?item_name=" + itemname, resp => {
        edit_box.then(template => {
            overlay_on(template
                .replaceAll("%itemname%", resp["name"])
                .replaceAll("%itemcost%", resp["cost"])
                .replaceAll("%itemamount%", resp["amount"])
            );
        })
    });
    loadItems()
}

function loadItems() {
    function items_callback(response) {
        var item_table = document.getElementById("items");
        item_table.innerHTML = "";
        bar.then(template => { item_table.innerHTML += template });
        response.forEach(item => {
            item_template.then(template => {
                item_table.innerHTML += template
                    .replaceAll("/item_name/", item["name"])
                    .replaceAll("/item_cost/", item["cost"])
                    .replaceAll("/item_amount/", item["amount"]);
                }
            )
                
        })
    }
    request("/shop/list", callback=items_callback)
}

function create() {
    create_box.then(box => { overlay_on(box); });
}

function exitForm() {
    overlay_off();
    loadItems();
}

function deleteitem(itemname) {
    fetch("/shop/delete/"+item_name, {
		"method":"DELETE"
	);
    overlay_off()
    loadItems()
}

document.addEventListener("DOMContentLoaded", loadItems())
document.addEventListener("submit", e => {
    var body = {};
	// TODO: submit override
    e.preventDefault();
	e.target.submit();
	// while (document.getElementById("hiddeniframe").innerHTML == "") {}
	loadItems();
	overlay_off();
})