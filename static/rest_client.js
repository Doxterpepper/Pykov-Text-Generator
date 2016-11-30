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
	var response = JSON.parse(requests.response);
	document.getElementById('corpus').value = response['text'];
	document.getElementById('title').value = response['title'];
}

function generate() {
}

function save_corpus(token) {
	var requests =new XMLHttpRequest();
	requests.open("POST", url+"/api/upload", false);
	corpus = document.getElementById('corpus').value;
	title = document.getElementById('title').value;
	if (corpus == "" || title == "")
	{
		error = "Please input text into both the title, and corpus fields."
		alert(error);
		return error;
	}
		var data = JSON.stringify({'token': token, 'title': title, 'corpus':corpus});
		ret = requests.send(data);
}
