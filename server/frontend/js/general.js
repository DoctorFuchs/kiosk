async function loadTemplate(path) {
	// return an template await response text => used to get templates, like overlays, ...
	// fetch response
	const response = await fetch(path);
	// turn into Promise<string>
	const template = await response.text();
	// return template
	return template;

}

document.cookie = "first=False"
