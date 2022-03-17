function overlay_on(content) {
    overlay_off();
    var overlay = document.createElement("div");
    var hidden_iframe = document.createElement("iframe");

    // hiddeniframe
    hidden_iframe.name = "hiddeniframe";
    hidden_iframe.hidden = true;
    

    // overlay
    overlay.classList.add("w3-modal");
    overlay.style.display = "block";

    overlay.innerHTML += hidden_iframe.outerHTML;
    overlay.innerHTML += content;
    
    document.body.appendChild(overlay); 
}

function overlay_off() {
    var elems = document.getElementsByClassName("w3-modal");
    for (let elem of elems) {
        elem.remove();
    }
}
