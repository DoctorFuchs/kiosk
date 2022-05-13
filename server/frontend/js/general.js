async function loadTemplate(path) {
	// return an template await response text => used to get templates, like overlays, ...
	// fetch response
	const response = await fetch(path);
	// turn into Promise<string>
	const template = await response.text();
	// return template
	return template;
}

function setCookie(key, value, max_age = 9999999999, expires) {
	document.cookie = `${key}=${value}; max-age=${max_age}; expires=${expires}`
}

async function loadIntro(resp) {
	var introConfig = await (await fetch("/api/intro")).json()
	var filename = (window.location.pathname).substring(window.location.pathname.lastIndexOf('/') + 1);
	var location = filename != "" ? filename.split(".")[0] : "index"
	var config = introConfig.options
	config.steps = introConfig.tours[location] ? introConfig.tours[location].steps : []
	config.steps = config.steps.map((step) => {
		return {
			...step,
			"element": document.querySelector(step.element)
		}
	})
	var intro = introJs().setOptions(config)
	intro.onskip(() => {
		window.location.href = "/"
	})
	intro.oncomplete(() => {
		window.location.href = introConfig.tours[location].next_page ? `${introConfig.tours[location].next_page}?intro` : "/"
	})
	resp(intro)
}

function startIntro(force = false) {
	loadingIntro.then((intro) => {
		if (force) {
			intro.start();
		} else {
			var pathname = window.location.pathname;
			var location = pathname.endsWith("/") ? pathname + "index.html" : pathname;
			if (location.endsWith("index.html")) {
				intro.start();
			} else {
				window.location.href = "/?intro";
			}
		}
	});
}

document.addEventListener("DOMContentLoaded", e => {
	var elem = document.getElementById("navigation-bar");
	var pathname = window.location.pathname
	var location = pathname.endsWith("/") ? pathname + "index.html" : pathname;

	Array.from(elem.children).forEach(child => {
		let path = child.href.split("/");
		if (location.endsWith(path[path.length - 1])) {
			child.firstChild.classList.add("w3-bottombar")
			child.firstChild.classList.add("w3-border-theme")
		}
	})

	loadingIntro = new Promise(loadIntro)

	if (new URLSearchParams(window.location.search).has("intro")) {
		if (!document.getElementById("greeting")) {
			startIntro(true)
		}
	}

	var close_greeting = document.querySelector("#close_greeting")
	if (close_greeting) {
		close_greeting.addEventListener("click", () => {
			startIntro();
		})
	}

})