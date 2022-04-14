async function loadTemplate(path) {
	// return an template await response text => used to get templates, like overlays, ...
	// fetch response
	const response = await fetch(path);
	// turn into Promise<string>
	const template = await response.text();
	// return template
	return template;

}

document.addEventListener("DOMContentLoaded", e => {
	var elem = document.getElementById("navigation-bar");
	var location = window.location.href.endsWith("/") ? "index.html" : window.location.href;

	Array.from(elem.children).forEach(child => {
		let path = child.href.split("/");
		if (location.endsWith(path[path.length-1])) {
			child.firstChild.classList.add("w3-bottombar")
			child.firstChild.classList.add("w3-border-theme")
		}
	})
})

