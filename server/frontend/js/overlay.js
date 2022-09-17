function overlay_on(content) {
    // show content (html like) in a overlay
    // kill all other overlays
    overlay_off_brutal();

    // create overlay object and hiddeniframe object
    var overlay = document.createElement("div");
    var hidden_iframe = document.createElement("iframe");

    // hiddeniframe => iframe as a target for forms
    hidden_iframe.name = "hiddeniframe";
	hidden_iframe.id = "hiddeniframe";
    hidden_iframe.hidden = true;

    // overlay => overlay to show the content
    overlay.classList.add("w3-modal");
    overlay.style.display = "block";

    // add iframe to overlay
    overlay.innerHTML += hidden_iframe.outerHTML;
    overlay.innerHTML += content;

    // append child to body
    document.body.appendChild(overlay);

    return overlay;
}

function overlay_off_brutal() {
    // remove all overlays
    var elems = document.getElementsByClassName("w3-modal");
    for (let elem of elems) {
        elem.remove();
    }
}

function overlay_off() {
    // hide all overlays
    var elems = document.getElementsByClassName("w3-modal");
    for (let elem of elems) {
        elem.style.display = "none";
    }
}
