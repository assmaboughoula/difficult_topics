import urllib2
import numpy as np
from sets import Set
import json

# data = urllib2.urlopen("http://times.cs.uiuc.edu/course/598f16/data/dblp-small.txt")

mylist = []
# for line in data:
# 	mylist.append(line)

with open('textretrieval_docs.json') as textretrieval_docs:
    data = json.load(textretrieval_docs)
for lect in data:
	for minute in data[lect]:
		mylist.append(minute)

num_docs = len(mylist)
corpus = np.array(mylist)
np.save('plsa_corpus.npy',corpus)

vocab = Set([])

for doc in corpus:
	# words = doc.split()
	words = doc
	uniques = Set(words)
	vocab = vocab | uniques

vocab_size = len(vocab)
alphabetized = list(vocab)
alphabetized.sort()
v = np.array(alphabetized)
np.save('vocabulary.npy',v)

term_doc_matrix = np.zeros([num_docs, vocab_size], dtype=np.int)

d=0
for doc in corpus:
	# words = doc.split()
	words = doc
	for w in words:
		w_index = alphabetized.index(w)
		term_doc_matrix[d][w_index] += 1
	d+=1
np.save('term_doc_matrix.npy',term_doc_matrix)

prob_w_in_D = term_doc_matrix.sum(axis=0)/float(term_doc_matrix.sum())
np.save('prob_w_in_D.npy',prob_w_in_D)