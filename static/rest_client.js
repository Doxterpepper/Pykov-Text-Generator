var url="http://localhost:4999"

function get_corpus(id, token) {
	var requests = new XMLHttpRequest();
	requests.open("POST", url+"/api/corpus", false);
	var data = JSON.stringify({"id": id, 'token': token});
	console.log(data);
	ret = requests.send(data);
	var text = requests.response;
	document.getElementById('corpus').value = text;
}
