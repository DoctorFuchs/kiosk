var edit_box = "<div><h1 style='font-size: 6vh'>BEARBEITUNG - %itemname%</h1>"+
"<iframe style='display:none' name='hiddenframe'></iframe>"+
"<form action='/api/shop/edit' target='hiddenframe' method='GET' onsubmit='overlay_off()'>"+
"<input required name='item_name_old' type='hidden' value='%itemname%'>"+
"<label class='edit-label' for='item_name_new'>Name</label><br>"+
"<input required pattern='[a-zA-Z0-9\\s]+' class='edit' id='item_name_new' name='item_name_new' value='%itemname%' type='text'><br>"+
"<label class='edit-label' for='item_cost_new'>Preis</label><br>"+
"<input required class='edit' id='item_cost_new' name='item_cost_new' value=%itemcost% type='number' min='0' step='0.01'><br>"+
"<label class='edit-label' for='item_amount_new'>Verfügbare Menge</label><br>"+
"<input required class='edit' id='item_amount_new' name='item_amount_new' value=%itemamount% type='number' min=0 step='1'><br>"+
"<button class='submit-button' type='submit'>Okay</button>"+
"<button class='delete' onclick='deleteitem(\"%itemname%\"); exitForm()' type='button' type='reset'>Löschen</button>"+
"<button class='exit' onclick='exitForm()' type='reset'>Exit</button>"+
"</form></div>"

var create_box = "<div><h1 style='font-size: 6vh'>ERSTELLUNG</h1>"+
"<iframe style='display:none' name='hiddenframe'></iframe>"+
"<form action='/api/shop/additem' target='hiddenframe' onsubmit='exitForm()' method='GET'>"+
"<label class='create-label' for='item_name_new'>Name</label><br>"+
"<input required pattern='[a-zA-Z0-9\\s]+' class='create' id='item_name' name='item_name' type='text' requiered=True></input><br>"+
"<label class='create-label' for='item_cost'>Preis</label><br>"+
"<input required class='create' id='item_cost' name='item_cost' type='number' min='0' step='0.01'><br>"+
"<label class='create-label' for='item_amount'>Verfügbare Menge</label><br>"+
"<input required class='create' id='item_amount' name='item_amount' type='number' min=0 step='1'><br>"+
"<button style='width: 48%' class='submit-button' type='submit'>Okay</button>"+
"<button style='width: 48%' class='exit' onclick='exitForm()' type='reset'>Exit</button>"+
"</form></div>"

var bar = "<tr class='header'>"+
"<th id='product_name' onclick='order(\"name\")'>Produktname</th>"+
"<th id='product_price' onclick='order(\"cost\")'>Preis</th>"+
"<th id='product_amount' onclick='order(\"amount\")'>Verfügbare Menge</th>"+
"</tr>"

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
}

function get_order() {
    return req_args.replaceAll("%sort%", _by).replaceAll("%revert%", _revert)
}

function edit(itemnumber) {
    var item = document.getElementById("item_"+String(itemnumber));
    var itemname = item.childNodes[0].textContent;
    var itemcost = item.childNodes[1].textContent.replace("€", "");
    var itemamount = item.childNodes[2].textContent;
    overlay_on(edit_box
        .replaceAll("%itemname%", itemname)
        .replaceAll("%itemcost%", itemcost)
        .replaceAll("%itemamount%", itemamount))
}

function loadItems() {
    function items_callback(response) {
        document.getElementById("item-loader").style.display = "none"
        let item = document.getElementById("item-table");
        let req =  reformat(response);
        item.innerHTML = ""
        item.innerHTML += bar
        for (let i = 0; i < req.length ; i++) {
            let req_ = req[i].split(",")
            req_[0] = req_[0].replaceAll("'", "").replaceAll("+", " ")
            req_[1] = req_[1].replaceAll("'", "")
            req_[2] = req_[2].replaceAll("'", "")
            item.innerHTML += "<tr class='item' id='item_"+i+"' onclick='edit("+i+")'><td class='left'>"+req_[0]+"</td><td>"+req_[1]+"€</td><td class='right'>"+req_[2]+"</td></tr>"
        }
        setTimeout(loadItems, 700)
    }
    request("/shop/list"+get_order(), callback=items_callback)
}

function create() {
    overlay_on(create_box)
}

function exitForm() {
    overlay_off();
}

function deleteitem(itemname) {
    request("/shop/delete?item_name="+itemname);
    overlay_off()
}

document.addEventListener("DOMContentLoaded", loadItems())
