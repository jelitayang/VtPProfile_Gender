#!/usr/bin/python

import json
import sys
import os.path


def load_dict(output):
	print "loading"
	json1_file = open(output)
	json1_str = json1_file.read()
	w = json.loads(json1_str)
	json1_file.close()
	print len(w.keys())
	return w

def read_file_withfullconfidence(filen):
	for word in filen.read().split():
		if word not in wordcount:
			wordcount[word] = 1.0
		else:
			wordcount[word] = 1.0
#	for k,v in wordcount.items():
#		print k, v

def read_file_withsomeconfidence(filen):
	for word in filen.readlines():
		w,f =  word.strip().split()
		#print w, " is ", f
		if word not in wordcount:
			wordcount[w] = f
		else:
			#only update if the confidence is higher
			if wordcount[w] < f:
				wordcount[w] = f
			
input= str(sys.argv[1])
output = str(sys.argv[2])
confidencefull = int(sys.argv[3])
wordcount=dict()

if (os.path.isfile(output)) :
	wordcount= load_dict(output)
	print len(wordcount.keys())


file=open(input,"r")


if(confidencefull):
	read_file_withfullconfidence(file)
else:
	read_file_withsomeconfidence(file)

print len(wordcount.keys())

file.close()	

with open(output, 'w') as f: f.write(json.dumps(wordcount))
