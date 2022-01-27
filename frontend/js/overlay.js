var db_error_overlay_text = "<div>" +
    "<h1 style='color: red'> DB ODER API FUNKTIONIERT NICHT RICHTIG!</h1><br><br>" +
    "<p style='color:red'>Bitte prüfen Sie die backend konsole für mehr Informationen.<br>Überprüfen Sie zudem, ob Ihre Konfigurationen richtig sind</h1>" +
    "</div>"
var greeting = `<div style='display:flex;flex-direction:column;justify-content:center'><h1>Anscheinend ist dies das erste Mal, dass dieses Programm ausgeführt wird.</h1><p>Bitte konfigurieren sie ihre Kontaktinformation wie in der Dokumentation beschrieben.</p><p>Passen sie gegebenenfalls auch die anderen Programmeinstellungen an.</p><button onclick="greeting_off()" style='padding:1rem'>OK</button></div>`

function overlay_on(content) {
    document.getElementById("overlay").innerHTML = content;
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

function greeting_off() {
    // fetch('/api/firstRun?readed=1'); /* currently not used, this is for only hide message in new windows after ok was clicked */
    overlay_off();
}