function countChildren(element) {
	var relem = element;
	return relem.childNodes.length;
}

function gotosite(site) {
	var content = document.getElementById("content");
	content.innerHTML = `<iframe src='${site}' frameborder='0' width='100%' height='100%' id='iframe' visibility='hidden' transition='visibility 1s ease'>`;
	loadingAnimation();
}
