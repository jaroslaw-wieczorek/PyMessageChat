function addchannel() {
	var channelname = prompt("Please enter the channel name:", "Lemons");

	if (channelname == null || channelname == "") {
		txt = "User cancelled the prompt.";
	} else {
		postchannel(channelname);
	}
}
function adduser() {
	var username = prompt("Please enter the name of the person you want to invite:", "Lemon_God");

	if (username == null || username == "") {
		txt = "User cancelled the prompt.";
	} else {
		adduserchannel(username);
	}
}
window.onload = function() {
	removechannellist();
	removemsglist();
	removeuserlist();
	httpGetAsync("http://127.0.0.1:5000/channels", loadchanlist);

	document.getElementById("inputbex").onkeydown = function(e) {
		sendmessage(e);
	};
	profilemodal();
};

function sendmessage(e) {
	if (e.keyCode == 13) {
		//alert(document.getElementById("msgtext").value);
		postmsg(document.getElementById("msgtext").value);
		var element = document.getElementById("msglisto");
		element.scrollTop = element.scrollHeight - element.clientHeight;
		document.getElementById("msgtext").value = "";
	}
}

function profilemodal() {
	// Get the modal
	var modal = document.getElementById("myprofilemodal");

	// Get the button that opens the modal
	var btn = document.getElementById("myprofilemodalbtn");

	// Get the <span> element that closes the modal

	// When the user clicks the button, open the modal
	btn.onclick = function() {
		modal.style.display = "flex";
	};

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
		if (event.target == modal) {
			modal.style.display = "none";
		}
	};
}

function loadchanlist(jsonstring) {
	removechannellist();
	var obj = JSON.parse(jsonstring);
	for (var i = 0; i < obj.channels.length; i++) {
		addachanneltolist(obj.channels[i].name);
	}
}
function loadmsgs(jsonstring) {
	removemsglist();
	var obj = JSON.parse(jsonstring);
	for (var i = 0; i < obj.messages.length; i++) {
		addamsgtolist(obj.messages[i].content, obj.messages[i].time, obj.messages[i].username, obj.messages[i].avatar);
	}
	var element = document.getElementById("msglisto");
	element.scrollTop = element.scrollHeight - element.clientHeight;
}
function loaduserlist(jsonstring) {
	removeuserlist();
	var obj = JSON.parse(jsonstring);
	for (var i = 0; i < obj.owners.length; i++) {
		addausertolist(obj.owners[i], "owner");
	}
	for (var i = 0; i < obj.users.length; i++) {
		addausertolist(obj.users[i], "user");
	}
}

function httpGetAsync(theUrl, callback) {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4 && xmlHttp.status == 200) callback(xmlHttp.responseText);
	};
	xmlHttp.open("GET", theUrl, true); // true for asynchronous
	xmlHttp.setRequestHeader("Authorization", "Bearer " + getCookie("access_token"));
	xmlHttp.send(null);
}

function postchannel(name) {
	xhr = new XMLHttpRequest();
	var url = "http://127.0.0.1:5000/channels/" + name;
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.setRequestHeader("Authorization", "Bearer " + getCookie("access_token"));

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 201) {
			//var json = JSON.parse(xhr.responseText);
			//console.log(json.email + ", " + json.name)
			//console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
				httpGetAsync("http://127.0.0.1:5000/channels/" + getCookie("channel") + "/messages", loadmsgs);
				httpGetAsync("http://127.0.0.1:5000/channels/" + getCookie("channel"), loaduserlist);
			}, delayInMilliseconds);
		} else {
			var json = JSON.parse(xhr.responseText);
			console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				console.log("DELAY");
				httpGetAsync("http://127.0.0.1:5000/channels", loadchanlist);
			}, delayInMilliseconds);
		}
	};
	var data = JSON.stringify({ owners: getCookie("username"), users: "" });
	xhr.send(data);
}

function adduserchannel(name) {
	xhr = new XMLHttpRequest();
	var url = "http://127.0.0.1:5000/channels/" + getCookie("channel");
	xhr.open("UPDATE", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.setRequestHeader("Authorization", "Bearer " + getCookie("access_token"));

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 201) {
			//var json = JSON.parse(xhr.responseText);
			//console.log(json.email + ", " + json.name)
			//console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
				httpGetAsync("http://127.0.0.1:5000/channels/" + getCookie("channel") + "/messages", loadmsgs);
				httpGetAsync("http://127.0.0.1:5000/channels/" + getCookie("channel"), loaduserlist);
			}, delayInMilliseconds);
		} else {
			var json = JSON.parse(xhr.responseText);
			console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				console.log("DELAY");
				httpGetAsync("http://127.0.0.1:5000/channels", loadchanlist);
			}, delayInMilliseconds);
		}
	};
	var data = JSON.stringify({ owners: getCookie("username"), users: name });
	xhr.send(data);
}

function postmsg(text) {
	xhr = new XMLHttpRequest();
	var url = "http://127.0.0.1:5000/channels/" + getCookie("channel") + "/message";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.setRequestHeader("Authorization", "Bearer " + getCookie("access_token"));

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 201) {
			//var json = JSON.parse(xhr.responseText);
			//console.log(json.email + ", " + json.name)
			//console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
				httpGetAsync("http://127.0.0.1:5000/channels/" + getCookie("channel") + "/messages", loadmsgs);
				httpGetAsync("http://127.0.0.1:5000/channels/" + getCookie("channel"), loaduserlist);
			}, delayInMilliseconds);
		} else {
			var json = JSON.parse(xhr.responseText);
			console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				console.log("DELAY");
				httpGetAsync("http://127.0.0.1:5000/channels", loadchanlist);
			}, delayInMilliseconds);
		}
	};
	var data = JSON.stringify({
		username: getCookie("username"),
		content: text,
	});
	xhr.send(data);
}

function deletechannel(name) {
	xhr = new XMLHttpRequest();
	var url = "http://127.0.0.1:5000/channels/" + name;
	xhr.open("DELETE", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.setRequestHeader("Authorization", "Bearer " + getCookie("access_token"));

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 201) {
			//var json = JSON.parse(xhr.responseText);
			//console.log(json.email + ", " + json.name)
			//console.log(json);
			console.log("Ready");

			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				console.log("DELAY");
				httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
				httpGetAsync("http://127.0.0.1:5000/channels/" + getCookie("channel") + "/messages", loadmsgs);
				httpGetAsync("http://127.0.0.1:5000/channels/" + getCookie("channel"), loaduserlist);
			}, delayInMilliseconds);
		} else {
			var json = JSON.parse(xhr.responseText);
			console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				console.log("DELAY");
				httpGetAsync("http://127.0.0.1:5000/channels", loadchanlist);
			}, delayInMilliseconds);
		}
	};
	var data = JSON.stringify({ owners: getCookie("username"), users: "" });
	xhr.send(data);
}

function httpGetsync(theUrl, callback) {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4 && xmlHttp.status == 200) callback(xmlHttp.responseText);
	};
	xmlHttp.open("GET", theUrl, false); // true for asynchronous
	xmlHttp.setRequestHeader("Authorization", "Bearer " + getCookie("access_token"));
	xmlHttp.send(null);
}

function clickedchannel(name) {
	httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
	httpGetAsync("http://127.0.0.1:5000/channels/" + name + "/messages", loadmsgs);
	httpGetAsync("http://127.0.0.1:5000/channels/" + name, loaduserlist);
	document.getElementById(name).className = "showhim container darker_channel_clicked";
	setCookie("channel", name);
}

function setCookie(cname, cvalue) {
	document.cookie = cname + "=" + cvalue + ";path=/";
}
function addachanneltolist(name) {
	var chanlist = document.getElementById("chanulisto"),
		div = document.createElement("div"),
		text = document.createElement("span"),
		spanhide = document.createElement("span"),
		button = document.createElement("button");

	div.id = name;
	text.innerHTML += name;
	div.className = "showhim container darker_channel";
	div.onclick = function() {
		clickedchannel(name);
	};
	button.innerHTML += "x";
	button.className = "w3-button w3-small w3-circle w3-red";
	button.onclick = function() {
		removechannel(name);
	};
	spanhide.className = "showme";

	spanhide.appendChild(button);
	div.appendChild(text);
	div.appendChild(spanhide);
	chanlist.appendChild(div);
}

function removechannel(name) {
	deletechannel(name);
}

function addamsgtolist(text, date, who) {
	var msglist = document.getElementById("msglisto"),
		messageContainer = document.createElement("div"),
		dataContainer = document.createElement("div"),
		body = document.createElement("div"),
		avatar = document.createElement("div"),
		texto = document.createElement("p"),
		datetime = document.createElement("span"),
		name = document.createElement("p");

	messageContainer.className = `message-container ${getCookie("username") === who ? "logged-user" : "another-user"}`;

	avatar.className = "avatar";
	avatar.style["background-image"] = `url(http://i.pravatar.cc/72?u=${who})`;
	texto.innerHTML += text;
	name.innerHTML += who;
	name.className = "username";

	body.appendChild(name);
	body.appendChild(texto);
	body.className = "message";

	datetime.innerHTML = date;
	datetime.classList = "datetime";
	dataContainer.classList = "data-container";

	dataContainer.appendChild(body);
	dataContainer.appendChild(datetime);
	messageContainer.appendChild(avatar);
	messageContainer.appendChild(dataContainer);

	msglist.appendChild(messageContainer);
}

function addausertolist(name, type) {
	let usrlist = document.getElementById("usrlistocolumn"),
		ownerslist = document.querySelector("#ownerlistocolumn"),
		div = document.createElement("div"),
		avatar = document.createElement("div"),
		nameo = document.createElement("p");

	nameo.innerHTML += name;

	avatar.className = "avatar";
	avatar.style["background-image"] = `url(http://i.pravatar.cc/72?u=${name})`;

	div.className = "container darker";

	div.appendChild(avatar);
	div.appendChild(nameo);

	type !== "owner" ? usrlist.appendChild(div) : ownerslist.appendChild(div);
}
function removeuserlist() {
	var usrlist = document.getElementById("usrlistocolumn");
	while (usrlist.firstChild) {
		usrlist.removeChild(usrlist.firstChild);
	}
	var ownerslist = document.getElementById("ownerlistocolumn");
	while (ownerslist.firstChild) {
		ownerslist.removeChild(ownerslist.firstChild);
	}
}
function removemsglist() {
	var myNode = document.getElementById("msglisto");
	while (myNode.firstChild) {
		myNode.removeChild(myNode.firstChild);
	}
}
function removechannellist() {
	var myNode = document.getElementById("chanulisto");
	while (myNode.firstChild) {
		myNode.removeChild(myNode.firstChild);
	}
}

function getCookie(cname) {
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(";");
	for (var i = 0; i < ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == " ") {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}