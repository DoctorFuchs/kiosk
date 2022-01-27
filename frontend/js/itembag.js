let itembag_pay_overlay = "<div>"

let itembag = []

function get_amount_from_itembag(item_name) {
    var index = itembag.findIndex(item=>item[0]===item_name);
    if (index === -1) {
        console.log("This item wasn't found")
        return "0"
    }
    else {
        return String(itembag[index][2])
    }
}

function itembag_remove(item_name, many=-1) {
	var index = itembag.findIndex(item=>item[0]===item_name);
    if (index === -1) {
        console.log("This item wasn't found")
    }
    else {
        if (many===-1) {
            itembag.splice(index, 1)
        }
        else {
            itembag[index][2] -= many
            if (itembag[index][2]<=0) {
                itembag_remove(item_name)
            }
        }
    }
    itembag_render()
}

function itembag_add(item_name, item_cost, item_amount) {
    // let template = "<div class='item'><h4>"+item_name+"</h4><span><p class='price' style='align: left'>"+item_cost+"€</p><p style='text-align: right; width: 30%'>"+item_amount+"</p></span></div>"
    // document.getElementById("itembag").innerHTML += template
    var index = itembag.findIndex(item=>item[0]===item_name);
    if (index === -1) {
        itembag.push([item_name, new Number(item_cost), new Number(item_amount)])
    }
    else {
        itembag[index][2]+= new Number(item_amount)
    }
    itembag_render()
}

function itembag_render(to_pay = false) {
    itembag_update()
    let elem = document.getElementById(to_pay?"to_pay_itembag":"itembag");
    sum = 0
    elem.innerHTML = itembag.length<=0?
    "<h1 style='font-size: 4vh; color: white'>Fügen sie Produkte durch anklicken hinzu</h1>": 
    "<h3 style=\"position:fixed;\">Warenkorb</h3><div style=\"height: 4vh;\"></div>"
    itembag.forEach(item => {
        item[1] < 0 ? itembag_remove(item[0], 1) : ""
        if (to_pay) {
            elem.innerHTML += "<div class='item'><h4>" + item[0] + "</h4><span>" + item[1] * item[2] + "€</span><span style='float: right'>" + item[2] + "</span></div>"
        }
        else {
            elem.innerHTML += "<div class='item' onclick='itembag_remove(\""+item[0]+"\", 1)'><h4>"+item[0]+"</h4><span>"+item[1]*item[2]+"€</span><span style='float: right'>"+item[2]+"</span></div>"
        }
        
        sum += item[1]*item[2]
    })
    document.getElementById("sum").innerText = sum + "€"
}

function itembag_pay() {
    overlay_on(itembag_pay_overlay)
    itembag_render(to_pay=true)
    request("")
}

function callback(response) {
    let item = document.getElementById("products");
    let req =  reformat(response);
    item.innerHTML = req.length<=0?
    "<h1 style='font-size: 8vh; color: white'>Keine Produkte vorhanden! Gehen sie zum Lager um weitere Produkte hinzuzufügen</h1>": ""
    for (let i = 0; i < req.length ; i++) {
        let req_ = req[i].split(",")
        req_[0] = req_[0].replaceAll("+", " ")
        req_[1] = req_[1].replaceAll("'", "")
        req_[2] = Number(req_[2].replaceAll("'", "").replaceAll(" ", "")) - Number(get_amount_from_itembag(req_[0].replaceAll("'", "")));
        item.innerHTML += '<div class="product" onclick="itembag_add('+String(req_[0])+","+String(req_[1])+','+(req_[2]>0 ? 1:0)+')"><h1 style="font-size: 8vh">'+String(req_[2])+'</h1><h4 style=\"font-size: 4vh\">'+req_[0].replaceAll("'", "")+'</h4><span class="price" style="font-size: 4vh">'+req_[1].replaceAll("'", "")+'€</span></div>'
        //item.innerHTML += "<tr class='item' id='item_"+i+"' onclick='edit("+i+")'><td class='left'>"+req_[0].replaceAll("+", " ")+"</td><td>"+req_[1]+"€</td><td class='right'>"+req_[2]+"</td></tr>"
    } 
}

function itembag_update() {
    request("/shop/list", callback)  
}


itembag_render()