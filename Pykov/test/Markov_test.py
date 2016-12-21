import Markov
import unittest
import re

class Markov_Test(unittest.TestCase):
	def test_gen_relation(self):
		sentence = "This is a dog"
		example = {
		  'This': ['is'],
		  'is': ['a'],
		  'a': ['dog']
		}
		gen = Markov.gen_relation(sentence)
		print("Sentence: " + Markov.gen_with_relations(gen, 10))
		self.assertEqual(example, gen)

	def test_relation_file(self):
		f = open('test.txt', 'r')
		text = f.read()
		f.close()
		print(Markov.gen_relation(text))
	
	def test_gen_words(self):
		corp = "This is quite a sentence and such"
		text = Markov.gen_with_text(corp, 10)
		print("test_gen_words: " + str(text))

if __name__ == '__main__':
	unittest.main()
