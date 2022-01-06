var port = "5000/";

function countChildren(element) {
	var relem = element;
	return relem.childNodes.length;
}

function apiGET(path){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "localhost"+port+path, false ); 
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function kasse(){
    document.getElementById("content")
        .innerHTML = '<iframe src="kasse.html" height=100% width=100%></iframe>';
}

function lager(){
    document.getElementById("content")
        .innerHTML = '<iframe src="lager.html" height=100% width=100%></iframe>';
}