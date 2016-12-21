import unittest
import requests

class API_Test(unittest.TestCase):
	def setUp(self):
		self.url = 'localhost:4999'
		sw = open('../SW.txt', 'r')
		self.corpus = sw.read()

	def test_upload_corpus(self):
		u_data = {
			'title': 'Star Wars episdoe IV',
			'corpus': self.corpus,
			'token': 'e68e4b8b9f426ef6bd220bcc53997849'
		}
		resp = requests.post(self.url + '/api/upload', data=u_data)
		if resp.status_code != 200:
			return False
if __name__ == '__main__':
	unittest.main()
