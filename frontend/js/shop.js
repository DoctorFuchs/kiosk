import general

function shop() {
	var content = document.getElementById("content")
	var items = general.apiGET("store")
	for (let item of items) {
		content.innerHTML += "<div class='store_item'><h3>"+item['name']+"</h3>"+
		"<button class='reduce' type='button'>+</button><input ><button class='add' type='button'>-</button></div>"
	}
}

