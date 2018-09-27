window.onload = function() {
	let user_myname = document.getElementById("MYNAME");
	user_myname.innerHTML = `${getCookie("username")}`;

	let current_channel = document.getElementById("currentChannel");
	current_channel.innerHTML = `Messages: ${getCookie("channel")}`;
}

window.setInterval(
function(){ 
	//let myHeaders = new Headers();
	//myHeaders.set("Authorization", `Bearer ${getCookie("refresh_token")}`);

	xhr = new XMLHttpRequest();
	var url = "http://127.0.0.1:5000/refresh";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.setRequestHeader("Authorization",`Bearer ${getCookie("refresh_token")}`);

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 200) {
			
			var json = JSON.parse(xhr.responseText);
			//console.log(json);
			console.log(json.access_token)
			setCookie('access_token', json.access_token);
			//setCookie('refresh_token', json.refresh_token);

			httpGetAsync(
				"http://127.0.0.1:5000/channels/" +
				getCookie("channel") +
				"/messages",
				loadmsgs
			);
		}
	};
	xhr.send(null);





}, 30000);







function addchannel() {
	var channelname = prompt("Please enter the channel name:", "Lemons");

	if (channelname == null || channelname == "") {
		txt = "User cancelled the prompt.";
	} else {
		postchannel(channelname);
	}
}

async function asyncFetchUsers() {
	// Fire both API requests at the same time

	let myHeaders = new Headers();
	myHeaders.set("Authorization", `Bearer ${getCookie("access_token")}`);

	let myInit = {
		method: "GET",
		headers: myHeaders,
		mode: "cors",
		cache: "default",
	};
	const channelUsers = fetch(
		`http://127.0.0.1:5000/channels/${getCookie("channel")}`,
		myInit
	);
	const allUsers = fetch("http://127.0.0.1:5000/users", myInit);

	const [channel, all] = await Promise.all([channelUsers, allUsers]);

	return { channel, all };
}
function adduser() {
	// console.log(asyncFetchUsers());

	console.log(getCookie("username"));

	let addusermodal = document.querySelector("#addusermodal");
	let addusermodalcontent = document.querySelector(".addusermodal-content");
	addusermodalcontent.innerHTML = "";

	let myHeaders = new Headers();
	myHeaders.set("Authorization", `Bearer ${getCookie("access_token")}`);

	let myInit = {
		method: "GET",
		headers: myHeaders,
		mode: "cors",
		cache: "default",
	};
	const channelUsers = fetch(
		`http://127.0.0.1:5000/channels/${getCookie("channel")}`,
		myInit
	);
	const allUsers = fetch("http://127.0.0.1:5000/users", myInit);

	Promise.all([
		channelUsers.then(response => response.json()),
		allUsers.then(response => response.json()),
	]).then(function(values) {
		const owners = new Set(values[0].owners);
		const allUsers = values[1].users.map(el => el.username);

		if (owners.has(getCookie("username"))) {
			addusermodal.style.display = "flex";
			createUserlistForUpdate(
				values[0],
				allUsers,
				addusermodal,
				addusermodalcontent
			);
		} else {
			addusermodal.style.display = "none";
			alert("Nie masz uprawnień do edycji tego kanału");
		}
	});
}

function createUserlistForUpdate(
	channelUsers,
	allUsers,
	addusermodal,
	addusermodalcontent
) {
	const users = new Set(channelUsers.users);
	const owners = new Set(channelUsers.owners);
	console.log(allUsers);

	for (const name in allUsers) {
		let elementToList = document.createElement("div");
		elementToList.className = "addusermodal-row";

		let img = document.createElement("div");
		img.className = "avatar";
		img.style["background-image"] = `url(http://i.pravatar.cc/72?u=${
			allUsers[name]
		})`;

		let username = document.createElement("p");
		username.innerHTML = `${allUsers[name]}`;

		let check_box_1 = document.createElement("input");
		check_box_1.type = "checkbox";
		check_box_1.value = "user";
		check_box_1.checked = users.has(allUsers[name]) ? true : false;
		check_box_1.className = "user";

		let check_box_2 = document.createElement("input");
		check_box_2.type = "checkbox";
		check_box_2.value = "user";
		check_box_2.checked = owners.has(allUsers[name]) ? true : false;
		check_box_2.className = "owner";

		elementToList.appendChild(username);
		elementToList.appendChild(check_box_1);
		elementToList.appendChild(check_box_2);

		addusermodalcontent.appendChild(elementToList);
	}

	let addbtn = document.createElement("button");
	addbtn.innerHTML = "Save";

	let addusermodalwrapper = document.querySelector(".addusermodal-wrapper");
	addusermodalwrapper.appendChild(addbtn);

	addbtn.onclick = () => {
		addusermodal.style.display = "none";
		addusermodalwrapper.removeChild(addbtn);
		prepareBodyFromUpdateUserList(
			document.querySelectorAll(".addusermodal-row")
		);
	};
}

function prepareBodyFromUpdateUserList(rows) {
	const body = {
		users: [],
		owners: [],
	};

	for (const row of rows) {
		const username = row.querySelector("p").textContent;

		row.querySelector(".user").checked ? body.users.push(username) : null;
		row.querySelector(".owner").checked ? body.owners.push(username) : null;
	}
	//body.users.length === 0 ? (body.users = null) : null;
  	//body.owners.length === 0 ? (body.owners = null) : null;

	let myHeaders = new Headers();
	myHeaders.set("Authorization", `Bearer ${getCookie("access_token")}`);
	myHeaders.set("Content-Type", "application/json; charset=utf-8");

	let myInit = {
		method: "PUT",
		headers: myHeaders,
		mode: "cors",
		cache: "default",
		body: JSON.stringify(body),
	};

	let myRequest = new Request(
		`http://127.0.0.1:5000/channels/${getCookie("channel")}`,
		myInit
	);

	fetch(myRequest)
		.then(response => {
			removeuserlist();
			return response.json();
		})
		.then(data => {
			let { owners, users } = data;
			if (owners !== undefined) {
				for (let i = 0; i < owners.length; i++)
					addausertolist(owners[i], "owner");
			}

			if (users !== undefined) {
				for (let i = 0; i < users.length; i++)
					addausertolist(users[i], "user");
			}
		})
		.catch(function error(error) {
			console.log("request failed", error);
			console.log("request failed", error.stack);

			alert("Sesja została zakończona, zaloguj się ponownie");
			//document.location.replace("http://127.0.0.1:5000");
		});
}

function getUsers() {
	let myHeaders = new Headers();
	myHeaders.set("Authorization", `Bearer ${getCookie("access_token")}`);
	myHeaders.set("Content-Type", "application/json; charset=utf-8");

	let myInit = {
		method: "GET",
		headers: myHeaders,
		mode: "cors",
		cache: "default",
	};

	return new Request("http://127.0.0.1:5000/users", myInit);
}

window.onclick = function(event) {
	if (event.target) {
		model = document.getElementById("profilemodal");
		addusermodal = document.getElementById("addusermodal");
		model.style.display = "none";
		addusermodal.style.display = "none";
	}
};

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

	let btn_logout = document.getElementById("MYNAME_logout");

	btn_logout.onclick = function() {
		modal.style.display = "none";

		xhr = new XMLHttpRequest();
		var url = "http://127.0.0.1:5000/logout";
		xhr.open("GET", url, true);

		xhr.setRequestHeader("Content-type", "application/json");
		xhr.setRequestHeader(
			"Authorization",
			"Bearer " + getCookie("access_token")
		);

		xhr.send(null);

		window.location = "/";
	};
	let avatar_label = document.getElementById("MYNAME_avatar");
	let name_label = document.getElementById("MYNAME_username");
	let email_label = document.getElementById("MYNAME_email");

	let myHeaders = new Headers();
	myHeaders.set("Authorization", `Bearer ${getCookie("access_token")}`);

	let myInit = {
		method: "GET",
		headers: myHeaders,
		mode: "cors",
		cache: "default",
	};

	let myRequest = new Request("/user", myInit);

	fetch(myRequest)
		.then(function(response) {
			return response.json();
		})
		.then(function(data) {
			avatar_label.style[
				"background-image"
			] = `url(http://i.pravatar.cc/72?u=${data.username})`;
			name_label.innerHTML = data.username;
			email_label.innerHTML = data.email;
		});

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
		addamsgtolist(
			obj.messages[i].content,
			obj.messages[i].time,
			obj.messages[i].username,
			obj.messages[i].avatar
		);
	}
	var element = document.getElementById("msglisto");
	element.scrollTop = element.scrollHeight - element.clientHeight;
}
function loaduserlist(jsonstring) {
	removeuserlist();
	let { owners, users } = JSON.parse(jsonstring);
	for (let i = 0; i < owners.length; i++) addausertolist(owners[i], "owner");
	for (let i = 0; i < users.length; i++) addausertolist(users[i], "user");
}

function httpGetAsync(theUrl, callback) {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
			callback(xmlHttp.responseText);
	};
	xmlHttp.open("GET", theUrl, true); // true for asynchronous
	xmlHttp.setRequestHeader(
		"Authorization",
		"Bearer " + getCookie("access_token")
	);
	xmlHttp.send(null);
}

function postchannel(name) {
	xhr = new XMLHttpRequest();
	var url = "http://127.0.0.1:5000/channels/" + name;
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.setRequestHeader(
		"Authorization",
		"Bearer " + getCookie("access_token")
	);
	//console.log("dupa");
	console.log(getCookie("access_token"));
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 201) {
			//var json = JSON.parse(xhr.responseText);
			//console.log(json.email + ", " + json.name)
			//console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
				httpGetAsync(
					"http://127.0.0.1:5000/channels/" +
						getCookie("channel") +
						"/messages",
					loadmsgs
				);
				httpGetAsync(
					"http://127.0.0.1:5000/channels/" + getCookie("channel"),
					loaduserlist
				);
			}, delayInMilliseconds);
		} else {
			//var json = JSON.parse(xhr.responseText);
			console.log(xhr.responseText);

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
	xhr.setRequestHeader(
		"Authorization",
		"Bearer " + getCookie("access_token")
	);

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 201) {
			//var json = JSON.parse(xhr.responseText);
			//console.log(json.email + ", " + json.name)
			//console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
				httpGetAsync(
					"http://127.0.0.1:5000/channels/" +
						getCookie("channel") +
						"/messages",
					loadmsgs
				);
				httpGetAsync(
					"http://127.0.0.1:5000/channels/" + getCookie("channel"),
					loaduserlist
				);
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
	var url =
		"http://127.0.0.1:5000/channels/" + getCookie("channel") + "/message";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.setRequestHeader(
		"Authorization",
		"Bearer " + getCookie("access_token")
	);

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && xhr.status == 201) {
			//var json = JSON.parse(xhr.responseText);
			//console.log(json.email + ", " + json.name)
			//console.log(json);
			var delayInMilliseconds = 500; //1 second
			setTimeout(function() {
				httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
				httpGetAsync(
					"http://127.0.0.1:5000/channels/" +
						getCookie("channel") +
						"/messages",
					loadmsgs
				);
				httpGetAsync(
					"http://127.0.0.1:5000/channels/" + getCookie("channel"),
					loaduserlist
				);
			}, delayInMilliseconds);
		} else if (xhr.readyState == 4 && (xhr.status == 400 || xhr.status == 401)) {
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
	xhr.setRequestHeader(
		"Authorization",
		"Bearer " + getCookie("access_token")
	);

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
				httpGetAsync(
					"http://127.0.0.1:5000/channels/" +
						getCookie("channel") +
						"/messages",
					loadmsgs
				);
				httpGetAsync(
					"http://127.0.0.1:5000/channels/" + getCookie("channel"),
					loaduserlist
				);
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
		if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
			callback(xmlHttp.responseText);
	};
	xmlHttp.open("GET", theUrl, false); // true for asynchronous
	xmlHttp.setRequestHeader(
		"Authorization",
		"Bearer " + getCookie("access_token")
	);
	xmlHttp.send(null);
}

function clickedchannel(name) {
	httpGetsync("http://127.0.0.1:5000/channels", loadchanlist);
	httpGetAsync(
		"http://127.0.0.1:5000/channels/" + name + "/messages",
		loadmsgs
	);
	httpGetAsync("http://127.0.0.1:5000/channels/" + name, loaduserlist);
	document.getElementById(name).className =
		"showhim container darker_channel_clicked";
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

	messageContainer.className = `message-container ${
		getCookie("username") === who ? "logged-user" : "another-user"
	}`;

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
