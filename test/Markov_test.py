import Markov
import unittest

class Markov_Test(unittest.TestCase):
	def test_gen_relation(self):
		sentence = "This is a dog"
		example = {
		  'This': ['is'],
		  'is': ['a'],
		  'a': ['dog']
		}
		gen, words = Markov.gen_relation(sentence)
		self.assertEqual(example, gen)
	
	def test_gen_words(self):
		corp = "This is quite a sentence and such"
		text = Markov.gen(corp, 10)
		print(text)

if __name__ == '__main__':
	unittest.main()
