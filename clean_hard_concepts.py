import string
import sys
import glob, os
import json
import nltk.tokenize
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer


def cleanHardConcepts(folderPath, exceptFiles, output):

	printable = set(string.printable)

	tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
	p_stemmer = PorterStemmer()
	en_stop = get_stop_words('en')
	en_stop.append("s")

	rawText = ""
	
	for file in os.listdir(folderPath):
		if file.endswith(".txt") and file not in exceptFiles:
			current = open(folderPath+'/'+file,'r')
			rawText += " "+current.read()
	
	printableText = filter(lambda x: x in printable, rawText)
	printableText = printableText.lower()
	
	tokens = tokenizer.tokenize(printableText)
	stopped_tokens = [i for i in tokens if not i in en_stop]
	text = [p_stemmer.stem(i) for i in stopped_tokens]
	cleanText = ' '.join(text)
	
	if len(output) != 0:
		f = open(folderPath+'/'+output, 'w')
		f.write(cleanText)
		f.close()
	else:
		f = open(folderPath+'/clean_hard_concepts.txt', 'w')
		f.write(cleanText)
		f.close()
	return

if (__name__ == "__main__"):
	cleanHardConcepts(sys.argv[1],sys.argv[2],sys.argv[3])
