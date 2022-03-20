class Itembag {
    constructor() {
        this.itembag = [];
        this.item_in_bag_template = loadTemplate("/shop/item_in_bag.html");
        this.item_out_bag_template = loadTemplate("/shop/item_out_bag.html");
        this.itembag_pay_dialog = loadTemplate("/shop/itembag_pay.html");
    }

    get_amount_from_itembag(item_name) {
        var index = this.itembag.findIndex(item => item["name"] === item_name);
        if (index >= 0) {
            return this.itembag[index]["amount"];
        }
        else {
            return 0;
        }
    }

    remove(item_name, many = -1) {
        var index = this.itembag.findIndex(item => item["name"] === item_name);

        if (index >= 0) {
            if (many === -1) {
                this.itembag.splice(index, 1);
            }
            else {
                this.itembag[index]["amount"] -= many;
                if (this.itembag[index]["amount"] <= 0) {
                    this.remove(item_name);
                }
            }
        }
        this.render();
    }

    add(item_name, item_amount) {
        request("/shop/item?item_name=" + item_name, resp => {
            var item_cost = resp["cost"];
            var index = this.itembag.findIndex(item => item["name"] === item_name);

            if (index === -1) {
                this.itembag.push({
                    "name": item_name,
                    "cost": new Number(item_cost),
                    "amount": new Number(item_amount)
                });
            }
            else {
                this.itembag[index]["amount"] += new Number(item_amount);
            }
            this.render();
        });
    }

    render() {
        this.update();
        var elem = document.getElementById("itembag");
        var sum = 0;

        elem.innerHTML = "";

        this.itembag.forEach(item => {
            this.item_in_bag_template.then(template => {
                elem.innerHTML += template
                    .replaceAll("/item_name/", item["name"])
                    .replaceAll("/item_cost/", item["cost"]*item["amount"])
                    .replaceAll("/item_amount/", item["amount"]);
            });
            
            sum += item["cost"] * item["amount"];
        });
        document.getElementById("sum").innerText = sum + "&euro;";
    };

    render_pay() {
        if (this.itembag.length == 0) { return; }
        this.itembag_pay_dialog.then(template => { overlay_on(template) });

        var product_list = document.getElementById("pay-dialog-itembag");
        var sum = 0;

        this.itembag.forEach(item => {
            this.item_in_bag_template.then(template => {
                product_list.innerHTML += template
                    .replaceAll("/item_name/", item["name"])
                    .replaceAll("/item_cost/", item["cost"])
                    .replaceAll("/item_amount/", item["amount"]);
            });

            sum += item["cost"]*item["amount"]
        });

        document.getElementById("pay-dialog-sum").innerHTML = sum+"&euro;"

    };

    pay_finish() {
        this.itembag.forEach(item => {
            request("/shop/buy?item_name=" + item["name"] + "&item_amount=" + item["amount"], a => { })
        })
        this.itembag = []
        this.render()
    }

    update() {
        request("/shop/list", resp => {
            var elem = document.getElementById("products");

            if (resp.lenght === 0) { return; }

            elem.innerHTML = ""

            resp.forEach(item => {
                this.item_out_bag_template.then(template => {
                    elem.innerHTML += template
                        .replaceAll("/item_name/", item["name"])
                        .replaceAll("/item_cost/", item["cost"])
                        .replaceAll("/item_amount/", item["amount"] - this.get_amount_from_itembag(item["name"]));
                })
            })
        })
    }
}

var ITEMBAG = new Itembag();

document.addEventListener("DOMContentLoaded", e => {
    ITEMBAG.render()
})


