import nltk.data
import sys

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open(sys.argv[1]) 
#"reviews2.txt")
for line in fp:
	for sentence in tokenizer.tokenize(line):
		print (sentence)
