class Itembag {
    // itembag class: itembag Manager
    constructor() {
        // initialize Itembag array
        this.itembag = [];

        // load tempaltes
        this.item_in_bag_template = loadTemplate("/shop/item_in_bag.html");
        this.item_out_bag_template = loadTemplate("/shop/item_out_bag.html");
        this.itembag_pay_dialog = loadTemplate("/shop/itembag_pay.html");
        this.item_in_paydialog_template = loadTemplate("/shop/item_in_paydialog.html");
        this.itembag_sum = loadTemplate("/shop/itembag_sum.html");
        this.add_item_template = loadTemplate("/shop/add_item.html")
    }

    get_amount_from_itembag(item_name) {
        // get amount of an item from item_name value
        // find index
        var index = this.itembag.findIndex(item => item["name"] === item_name);
        if (index >= 0) {
            // if index found
            return this.itembag[index]["amount"];
        }
        else {
            // if index is not found return 0
            return 0;
        }
    }

    remove(item_name, many = -1) {
        /* remove item_name from itembag.
        By default it deletes the item from itembag
        if many is given */
        var index = this.itembag.findIndex(item => item["name"] === item_name);

        if (index >= 0) {
            // if item found
            if (many === -1) {
                // if many is -1 (it's the default) it deletes the item
                this.itembag.splice(index, 1);
            }
            else {
                // if many is not -1 it reduce the amount by many
                this.itembag[index]["amount"] -= many;
                if (this.itembag[index]["amount"] <= 0) {
                    this.itembag.splice(index, 1);
                }
            }
        }
        this.render();
    }

    add(item_name, item_amount) {
        /*add x items, where x is the item_amount arguments,
         of item_name*/

        // request the server to get the item_cost
        request("/shop/item?item_name=" + item_name, resp => {
            // save item cost in item_cost var
            var item_cost = resp["cost"];

            // find index by item_name
            var index = this.itembag.findIndex(item => item["name"] === item_name);

            if (resp["amount"] == 0 || item_amount > resp["amount"]) { return ; }

            if (index === -1) {
                // if not found add item to itembag
                this.itembag.push({
                    "name": item_name,
                    "cost": new Number(item_cost),
                    "amount": new Number(item_amount)
                });
            }
            else {
                // if found add item_amount to existing item
                if ( resp["amount"] < this.itembag[index]["amount"] + item_amount ) {
                    item_amount = resp["amount"] - this.itembag[index]["amount"]
                }
                this.itembag[index]["amount"] += new Number(item_amount);
            }
            // re-render the itembag to make changes visible
            this.render();
        });
    }

    render() {
        // (re-)render the itembag
        // update itembag
        this.update();
        // get itembag
        var elem = document.getElementById("itembag");
        var sum = 0;

        // clear itembag
        elem.innerHTML = "";

        // for each item in itembag render template
        this.itembag.forEach(item => {
            // take item_in_bag_tempate
            this.item_in_bag_template.then(template => {
                // replace item_values in template with item (from this.itembag.forEach loop)
                elem.innerHTML += template
                .replaceAll("/item_name/", decodeURIComponent(item["name"]))
                .replaceAll("/item_name_encoded/", item["name"])
                .replaceAll("/item_cost/", Math.round(item["cost"] * item["amount"] * 100) / 100)
                .replaceAll("/item_amount/", item["amount"]);
            });
            // add sum
            sum += item["cost"] * item["amount"];
        });
        // write sum to sum item
        document.getElementById("sum").innerText = Math.round(sum*100)/100 + "€";
    };

    render_pay() {
        // create overlay
        this.itembag_pay_dialog
            .then(async template => {
                // render items to pay dialog (it also creates the pay dialog)
                var template = template

                // if itembag is empty return
                if (this.itembag.length == 0) { return; }

                // get product list in pay dialog
                var sum = 0;

                // for each item in itembag render template
                var product_list_elem = ""
                await this.itembag.forEach(async item => {
                    // take item_in_bag_tempate
                    await this.item_in_paydialog_template.then(template => {
                        // replace item_values in template with item (from this.itembag.forEach loop)
                        product_list_elem += template
                            .replaceAll("/item_name/", decodeURIComponent(item["name"]))
                            .replaceAll("/item_name_encoded/", item["name"])
                            .replaceAll("/item_cost/", item["cost"])
                            .replaceAll("/item_amount/", item["amount"]);
                    });

                    // add sum
                    sum += item["cost"]*item["amount"]
                });
                template = template.replaceAll("/product_list_elem/", product_list_elem)

                // write sum to pay dialog
                var product_sum_elem
                await this.itembag_sum.then(template => {  
                    product_sum_elem = template.replaceAll("/sum/", `${Math.round(sum*100)/100}€`) 
                })

                template = template.replaceAll("/product_sum_elem/", product_sum_elem)
                return template;
            })
            .then(overlay => {
                overlay_on(overlay);
                document.querySelector('#bar').focus()
            })
    };

    pay_finish() {
        // finish pay dialog
        this.itembag.forEach(item => {
            // send buy requests to api
            request("/shop/buy?item_name=" + item["name"] + "&item_amount=" + item["amount"], null, false)
        })
        // clear item_bag
        this.itembag = []
        // re-render itembag to make changes visible
        this.render()
    }

    update() {
        // render available items from storage / list
        // get element to render the products
        var elem = document.getElementById("products");

        // fetch shop/list
        request("/shop/list", resp => {
            // if there are no items return
            if (resp.lenght === 0) { return; }

            // clear items
            elem.innerHTML = ""

            // render a template for each item in resp
            resp.forEach(item => {
                this.item_out_bag_template.then(template => {
                    elem.innerHTML += template
                        .replaceAll("/item_name/", decodeURIComponent(item["name"]))
                        .replaceAll("/item_name_encoded/", item["name"])
                        .replaceAll("/item_cost/", item["cost"])
                        .replaceAll("/item_amount/", item["amount"] - this.get_amount_from_itembag(item["name"]));
                })
            })
            // add placeholder to add new products
            this.add_item_template.then(template => {elem.innerHTML += template})
        })
    }
}

// create ITEMBAG constant
const ITEMBAG = new Itembag();

// render itembag when DOMContent is loaded
document.addEventListener("DOMContentLoaded", e => {
    ITEMBAG.render()
})
