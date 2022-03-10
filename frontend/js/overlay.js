function overlay_on(content = null) {
    if (content != null) {
        document.getElementById("overlay").innerHTML = content;
    }
    document.getElementById("overlay").style.display = "block";
    setTimeout(() => {
        document.getElementById("overlay").style.opacity = "1";
    }, 0)
}

function overlay_off() {
    document.getElementById("overlay").style.opacity = "0";
    setTimeout(function () {
        document.getElementById("overlay").style.display = "none";
    }, 300);
}

function removeClassesOnObejects(class_name) {
    var matches = document.getElementsByClassName(class_name);
    while (matches.length > 0) {
        matches[0].classList.remove(class_name);
    }
}
