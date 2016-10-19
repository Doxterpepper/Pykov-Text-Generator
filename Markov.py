import random
import re

def gen_relation(text):
	relations = {}
	words = re.split('\s+', text)
	for i in range(len(words) - 1):
		if words[i] in relations:
			relations[words[i]].append(words[i+1])
		else:
			relations[words[i]] = [words[i+1]]
	return (relations, words)

def gen(text, num, relations=None):
	if relations == None:
		relations, words = gen_relation(text)
	else:
		words = re.split('\s+', text)
	words = [words[random.randint(0, len(words) - 1)]]
	for i in range(num):
		if not words[-1] in relations:
			return ' '.join(words) + ' ' + gen(text, num-i, relations)
		arr = relations[words[-1]]
		n_word = arr[random.randint(0, len(arr)-1)]
		words.append(n_word)
	return ' '.join(words)
