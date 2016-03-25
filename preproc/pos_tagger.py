import nltk
import sys

sen_separated_text = open(sys.argv[1])
for line in sen_separated_text:
	text = nltk.word_tokenize(line) 
	print('\t'.join(map(str,nltk.pos_tag(text))))