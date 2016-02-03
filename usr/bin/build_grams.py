#!/usr/bin/python
import io,json
import sys
import pprint
from nltk.util import ngrams
#from collections import Counter

import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")

dir = "dict"

def load_dict(input):
	json1_file = open(input)
	json1_str = json1_file.read()
	jdata = json.loads(unicode(json1_str))
	json1_file.close()
	return jdata

def build_grams(w,prob,grams):
	freqitem =[]
	p = float(prob)
	if w not in grams:
		freqitem.append(1)
		freqitem.append(p)
		grams[w] = freqitem
	else:
		grams[w][0] +=1
		if grams[w] < p:
			grams[w][1] = p
	
def get_ngrams (col, num, grams,prefix, suffix):	

	for items  in col.items():
	#print items

		gr = ngrams(items[0].encode('utf8'),num)
	
		i = 0
		ending =''
		for gram in gr:
			w = ''.join(map(str,gram))
			ending = w
			build_grams(w,str(items[1]).encode('ascii'),grams)
			if (i==0):
				build_grams(w,str(items[1]).encode('ascii'),prefix)
			i+=1
		build_grams(w,str(items[1]).encode('ascii'),suffix)	
		
def dump_json (col, filename):
	with io.open(filename, 'w') as f:
		f.write(unicode(json.dumps(col, ensure_ascii=False)))	
	
def prettyprint_file(col,filename)	:
	di = col.items()
	di.sort(key=lambda (k,d): (d[0], d[1]), reverse=True)
	with open(dir +"/" + filename + ".txt", 'wt') as out:
		pprint.pprint(di, stream=out)	
	#with io.open(filename + ".json", 'w', encoding='utf-8') as f:
	
	dump_json(col, dir + "/" + filename + ".json")
	
	#return di	


def init (filename, ext):	
	col=load_dict(filename)
	
	for x in range(2, 5):
		gr = {}
		prefix ={}
		suffix = {}
		
		get_ngrams(col,x,gr, prefix, suffix)
	#print twog
	#print prefix
	#print suffix
		#jsonfile =  ext + str(x) + ".json"
	
		prettyprint_file(prefix, ext+  "_prefix_" + str(x) )
		prettyprint_file(suffix, ext + "_suffix_" + str(x))	
		
		prettyprint_file(gr, ext + "_ngram_" + str(x) )			
	
		#print p_suf
		
		#with open(ext + "_suffix_" + str(x) + ".json", 'w') as f: f.write(json.dumps(suffix))
		#with open(ext + "_prefix_" + str(x) + ".json", 'w') as f: f.write(json.dumps(prefix))
		#with open(ext + "_ngram_" + str(x) + ".json", 'w') as f: f.write(json.dumps(gr))

def get_unique_dict(col1,col2):
	dict1 = {}
	for i in col1.keys():
		if i not in col2.keys():
			dict1[i] = col1[i]
				
	return dict1
	
def find_unique_from_loading(x, ext ):

	file1 = dir + "/" + "female_" +  ext + "_"  + str(x) + ".json"
	#print file1
	col1 = load_dict(file1)
		
	file2 = dir + "/" + "male_" +  ext+  "_" + str(x) + ".json"
	#print file2
	col2 = load_dict(file2)
		
	dict1 = get_unique_dict(col1,col2)
	dict2 = get_unique_dict(col2,col1)
		
		
	prettyprint_file(dict1,  "female_unique_" + ext + "_" + str(x) )		
	prettyprint_file(dict2,  "male_unique_" + ext + "_" + str(x) )	

def find_unique ():
		
	for x in range(2, 5):
		find_unique_from_loading (x, "prefix")
		find_unique_from_loading (x, "suffix")
		find_unique_from_loading (x, "ngram")
			
	
init("female_names.json", "female")	
init("male_names.json", "male")	

find_unique()
	


