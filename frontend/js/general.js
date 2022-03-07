function countChildren(element) {
	var relem = element;
	return relem.childNodes.length;
}

document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".right-navbar-item > li > a[href], .dashboard_nav > ul > a").forEach((element) => {
		element.addEventListener("click", (event) => {
			event.preventDefault()
			gotosite(event.target.href)
		})
	})
})

function gotosite(site) {
	window.location.href = site
}

function toggleFullScreen() {
	if (!document.fullscreenElement) {
		document.documentElement.requestFullscreen();
	} else {
		if (document.exitFullscreen) {
			document.exitFullscreen();
		}
	}
}

function getCookie(cname) {
	let name = cname + "=";
	let decodedCookie = decodeURIComponent(document.cookie);
	let ca = decodedCookie.split(';');
	for (let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

addEventListener("DOMContentLoaded", e => {
	getCookie("fullscreen") === "1" ? toggleFullScreen : "";
})
