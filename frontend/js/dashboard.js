function dashboard() {
	var content = document.getElementById("content")
	content.innerHTML = ""
	content.innerHTML = "<nav></nav>"
}

function datum() {
	var date = new Date(),
		day = date.getDate(),
		month = date.getMonth(),
		year = date.getFullYear();
	day = fuehrendeNull(day);
	month = fuehrendeNull(month);
	year = year.toString().substr(2, 2);
	document.getElementById('datum')
		.innerHTML = day + "." + month + "." + year;

}

function uhrzeit() {
	var jetzt = new Date(),
		h = jetzt.getHours(),
		m = jetzt.getMinutes(),
		s = jetzt.getSeconds();
	h = fuehrendeNull(h);
	m = fuehrendeNull(m);
	s = fuehrendeNull(s);
	document.getElementById('uhr')
		.innerHTML = h + ':' + m + ':' + s;
	setTimeout(uhrzeit, 500);
}

function fuehrendeNull(zahl) {
	zahl = (zahl < 10 ? '0' : '') + zahl;
	return zahl;
}
// document.addEventListener('DOMContentLoaded', createNotification('<span id=uhr></span>', ''))
document.addEventListener('DOMContentLoaded', uhrzeit);
document.addEventListener('DOMContentLoaded', datum);