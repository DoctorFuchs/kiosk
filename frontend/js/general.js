function countChildren(element) {
	var relem = element;
	return relem.childNodes.length;
}

function gotosite(site) {
	var content = document.getElementById("content");
	content.innerHTML = `<iframe src='${site}' frameborder='0' width='100%' height='100%' id='iframe' style='opacity:0; transition:opacity 0.3s ease;'>`;
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

