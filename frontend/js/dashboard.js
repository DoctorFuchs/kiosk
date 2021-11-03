function dashboard() {
	let content = document.getElementById("content")
	content.innerHTML = ""
	content.innerHTML = "<nav></nav>"
}

function date() {
	let now = new Date(),
		day = now.getDate(),
		month = now.getMonth(),
		year = now.getFullYear();
	day = reformat(day);
	month = reformat(month);
	year = year.toString().substr(2, 2);
	document.getElementById('date')
		.innerHTML = day + "." + month + "." + year;

}

function time() {
	let now = new Date(),
		h = now.getHours(),
		m = now.getMinutes(),
		s = now.getSeconds();
	h = reformat(h);
	m = reformat(m);
	s = reformat(s);
	document.getElementById('time')
		.innerHTML = h + ':' + m + ':' + s;
	setTimeout(time, 100);
}

function reformat(number) {
	number = (number < 10 ? '0' : '') + number;
	return number;
}

document.addEventListener('DOMContentLoaded', date);
document.addEventListener('DOMContentLoaded', time);