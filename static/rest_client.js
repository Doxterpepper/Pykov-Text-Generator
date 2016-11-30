var url="http://localhost:4999"

function clear_corpus() {
	document.getElementById('corpus').value = "";
	document.getElementById('title').value = "";
}

function get_corpus(id, token) {
	var requests = new XMLHttpRequest();
	requests.open("POST", url+"/api/corpus", false);
	var data = JSON.stringify({"id": id, 'token': token});
	ret = requests.send(data);
	var text = JSON.parse(requests.response);
	document.getElementById('corpus').value = text['text'];
	document.getElementById('title').value = text['title'];
}

function generate() {
	var requests = new XMLHttpRequest();
	requests.open("POST", url+"/api/gen", false);
	var text = document.getElementById('corpus').value;
	var num = document.getElementById('controls').childNodes[1].value;

	num = parseInt(num, 10);
	//console.log(typeof(num));
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
	document.getElementById('generated').childNodes[1].innerText = response["corpus"];
}

function save_corpus() {
	
}
