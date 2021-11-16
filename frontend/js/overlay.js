var db_error_overlay_text = "<div>" +
    "<h1 style='color: red'> DB ODER API FUNKTIONIERT NICHT RICHTIG!</h1><br><br>" +
    "<p style='color:red'>Bitte prüfen Sie die backend konsole für mehr Informationen.<br>Überprüfen Sie zudem, ob Ihre Konfigurationen richtig sind</h1>" +
    "</div>"

var tutorial_overlay_slide_1 = "<div>" +
    "<h1>Tutorial</h1>" +
    "<p>Willkommen beim Tutorial<br>Wenn Sie fragen zu diesem Programm haben, wenden Sie sich bitte an github.com/doctorfuchs" +
    "<br></p>" +
    "<button onclick='overlay_on(tutorial_overlay_slide_2); document.getElementById(\"nav\").classList.add(\"tutorial-foreground\")'>Let's go</button><button onclick='overlay_off(), removeClassesOnObejects(\"tutorial-foreground\")'>Exit</button></div>"

var tutorial_overlay_slide_2 = "<div style='transform: translate(-50vw, -40vh)'>" +
    "<h1>Tutorial: Schritt 1 - Navigationsbar</h1>" +
    "<p>Das ist die Navigationsbar.<br> Wenn Sie in ein anderes Menü wollen, dann kommen Sie hier am schnellsten voran." +
    "<br></p>" +
    "<button onclick='overlay_off(); removeClassesOnObejects(\"tutorial-foreground\")'>Exit</button></div>"

function overlay_on(content) {
    document.getElementById("overlay").innerHTML = content;
    document.getElementById("overlay").style.display = "block";
    document.getElementById("overlay").style.opacity = "1";
}

function overlay_off() {
    document.getElementById("overlay").style.opacity = "0";
    setTimeout(function() {document.getElementById("overlay").style.display = "none";}, 300);
}

function removeClassesOnObejects(class_name) {
    var matches = document.getElementsByClassName(class_name);
    while (matches.length > 0) {
        matches[0].classList.remove(class_name);
    }
}

function tutorial() {
    overlay_on(tutorial_overlay_slide_1)
}