function overlay_on(content) {
    overlay_off_brutal();
    var overlay = document.createElement("div");
    var hidden_iframe = document.createElement("iframe");

    // hiddeniframe
    hidden_iframe.name = "hiddeniframe";
	hidden_iframe.id = "hiddeniframe";
    hidden_iframe.hidden = true;
    

    // overlay
    overlay.classList.add("w3-modal");
    overlay.style.display = "block";

    overlay.innerHTML += hidden_iframe.outerHTML;
    overlay.innerHTML += content;
    
    document.body.appendChild(overlay); 
}

function overlay_off_brutal() {
    var elems = document.getElementsByClassName("w3-modal");
    for (let elem of elems) {
        elem.remove();
    }
}

function overlay_off() {
    var elems = document.getElementsByClassName("w3-modal");
	console.log("Hey")
    for (let elem of elems) {
        elem.style.display = "none";
    }
}
