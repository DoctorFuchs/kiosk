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
	document.querySelectorAll(".right-navbar-item > li > a").forEach((element) => {
		element.classList.remove("active")
	})
	document.querySelectorAll(`.right-navbar-item > li > a`).forEach((element) => {
		if (element.href == site) {
			element.classList.add("active")
		}
	})
	document.getElementById("content").innerHTML = `<iframe src='${site}' frameborder='0' width='100%' height='100%' id='iframe' style='opacity:0; transition:opacity 0.3s ease;'>`;
	loadingAnimation();
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