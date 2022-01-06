

function createNotification(title, content) {
	document.getElementById("notifications").innerHTML += "<div class='notificationbox' onclick='expand(" + String(countChildren(document.getElementById("notifications")) + 1) + ")'><h1>" + title + "</h1><div class='expand' id=" + String(countChildren(document.getElementById("notifications")) + 1) + ">" + content + "</div></div>";
}

function deleteAllNotifications() {
	document.getElementById("notifications").innerHTML = "";
}

function deexpand(elementnumber) {
	var element = document.getElementById(String(elementnumber));
	if (element != null) {
		element.style.display = "none"
		element.style.height = "-10%"
	}
}

function deexpandAll() {
	for (let i = 1; i < countChildren(document.getElementById("notifications")) + 1; i++) {
		deexpand(i)
	}
}


function expand(elementnumber) {
	deexpandAll()
	var element = document.getElementById(String(elementnumber));
	element.style.display = "flex"
	element.style.height = "100%"
}

function hideNotifications() {
	var not = document.getElementById("notifications")
	not.style.display = "none"
}

function showNotifications() {
	var not = document.getElementById("notifications")
	not.style.display = "block"
}

