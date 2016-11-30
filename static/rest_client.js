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
}

function save_corpus() {
	
}
