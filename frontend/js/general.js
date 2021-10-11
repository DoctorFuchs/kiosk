let port = 8080;

function countChildren(element) {
	return element.childNodes.length;
}

function apiGET(path){
    fetch("http://localhost:"+String(port)+"/"+path)
        .then(response => response.text())
}
