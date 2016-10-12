import nltk
import sys

sen_separated_text = open(sys.argv[1])
#outfile = open(sys.argv[2], 'w')
count = 0

for line in sen_separated_text:
	##if count > 1000:
		##break
	text = nltk.word_tokenize(line) 
	if len(sys.argv) == 2:
		print('\t'.join(map(str,nltk.pos_tag(text))))
	elif len(sys.argv) == 3: # print CONLL format
		wordID = 1
		for item in nltk.pos_tag(text):
			#outfile.write("{0}\t{1}\t_\t{2}\t{2}\t_\n".format(wordID, item[0], item[1]))
			print("{0}\t{1}\t_\t{2}\t{2}\t_".format(wordID, item[0], item[1]))
			wordID += 1
		#outfile.write('\n')
		print

	count += 1

#outfile.close()