
function overlay_on(content=null) {
    if (content != null) {
        document.getElementById("root").innerHTML += content
    }
}

function overlay_off() {
    var elems = document.getElementsByClassName("w3-modal");
    for (var i = 0; i < elems.length; i++) {
        elems.item(i).style.display = "none";
    }
}

function removeClassesOnObejects(class_name) {
    var matches = document.getElementsByClassName(class_name);
    while (matches.length > 0) {
        matches[0].classList.remove(class_name);
    }
}
