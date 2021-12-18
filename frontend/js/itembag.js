function itembag_remove(item_name) {
			
}

function itembag_add(item_name, item_cost, item_amount) {
    let template = "<div class='item'><h4>"+item_name+"</h4><span><p class='price' style='align: left'>"+item_cost+"€</p><p style='text-align: right; width: 30%'>"+item_amount+"</p></span></div>"
    document.getElementById("itembag").innerHTML += template
}

function callback(response) {
    let item = document.getElementById("products");
    let req =  reformat(response);
    item.innerHTML = req.length==0?"<h1 style='font-size: 8vh; color: white'>Keine Produkte vorhanden! Gehen sie zum Lager um weitere Produkte hinzuzufügen</h1>": ""
    for (let i = 0; i < req.length ; i++) {
        let req_ = req[i].split(",")
        req_[0] = req_[0].replaceAll("'", "") 
        item.innerHTML += '<div class="product" onclick="itembag_add('+req[0].replaceAll("+", " ")+')"><h1 style="font-size: 8vh">'+req_[2]+'</h1><h4 style=\"font-size: 4vh\">'+req_[0].replaceAll('+', " ")+'</h4><span class="price" style="font-size: 4vh">'+req_[1]+'€</span></div>'
        //item.innerHTML += "<tr class='item' id='item_"+i+"' onclick='edit("+i+")'><td class='left'>"+req_[0].replaceAll("+", " ")+"</td><td>"+req_[1]+"€</td><td class='right'>"+req_[2]+"</td></tr>"
    } 
}

request("/shop/list", callback) 

