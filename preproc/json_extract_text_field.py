import json

counter = 0
data = []
with open('yelp_academic_dataset_review.json') as f:
	for line in f:
	#counter = counter + 1
	#if counter < 20:
	#print line

	#newFile.write(json.loads(line)["text"])
		print (json.loads(line)["text"])
	#else:
	#	break

	#print data