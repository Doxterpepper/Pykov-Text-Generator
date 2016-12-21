var url="http://localhost:5000"
var last_index = null;

function clear_corpus() {
	document.getElementById('corpus').value = "";
	document.getElementById('title').value = "";
}

function get_corpus(select, token) {
	if (last_index == null) {
		last_index = select.selectedIndex;
		return;
	}
	else if (last_index == select.selectedIndex) {
		return;
	}
	last_index = select.selectedIndex;
	var selected = document.querySelector("select").value;
	var id = selected[1];
	if (id < 3) {
	  token = null;
	}
	var requests = new XMLHttpRequest();
	requests.open("POST", url+"/api/corpus", false);
	var data = JSON.stringify({"id": id, 'token': token});
	ret = requests.send(data);
	var response = JSON.parse(requests.response);
	document.getElementById('corpus').value = response['text'];
	//document.getElementById('title').value = response['title'];
}

function generate() {
	var requests = new XMLHttpRequest();
	requests.open("POST", url+"/api/gen", false);
	var text = document.getElementById('corpus').value;
	var num = document.getElementById('wordcount').value;

	num = parseInt(num, 10);
	console.log(typeof(num));
	if (isNaN(num)) {
		alert("Invalid input");
		return;
	}
	var data = JSON.stringify({
		"corpus": text,
		"n": num
	});
	requests.send(data);
	var response = JSON.parse(requests.response);
	console.log(response["corpus"]);
	document.getElementById('generated').value = response["corpus"];
}

function save_corpus(token) {
	var requests =new XMLHttpRequest();
	requests.open("POST", url+"/api/upload", false);
	corpus = document.getElementById('corpus').value;
	title = prompt("What would you like to name this?");
	console.log(title);
	console.log(title);
	console.log(token);
	if (corpus == "")
	{
		error = "Please input text into corpus field."
		alert(error);
		return error;
	}
	var data = JSON.stringify({'token': token, 'title': title, 'corpus':corpus});
	ret = requests.send(data);
}
