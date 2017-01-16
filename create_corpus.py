import glob, os
import pysrt
import json
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import nltk.tokenize
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import csv


tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()
en_stop = get_stop_words('en')
en_stop.append("s")
texts = []
doctexts = {}

for file in os.listdir("textretrieval_srt"):
    if file.endswith(".srt"):
        current = pysrt.open('textretrieval_srt/'+file)
        t = file.split()
        lecture = t[0]+t[1]+t[2]
        buckets = []
        for i in range(len(current)):
            minute = current[i].start.minutes
            if len(buckets)>minute:
                buckets[minute] = buckets[minute]+' '+current[i].text
            else:
                buckets.extend(['']*(1+minute-len(buckets)))
                buckets[minute] = buckets[minute]+current[i].text

        doctexts[lecture] = [[]]*len(buckets)
        for j in range(len(buckets)):
            doc = buckets[j]
            raw = doc.lower()
            tokens = tokenizer.tokenize(raw)
            stopped_tokens = [i for i in tokens if not i in en_stop]
            text = [p_stemmer.stem(i) for i in stopped_tokens]
            #text = [p_stemmer.stem(i) for i in tokens]
            texts.append(text)
            doctexts[lecture][j] = text

with open('textretrieval_docs.json', 'w') as fp:
    json.dump(doctexts, fp, sort_keys=True, indent=4)


#print len(texts)
dictionary = corpora.Dictionary(texts)
print dictionary
corpus = [dictionary.doc2bow(text) for text in texts]
np.save('lda_corpus.npy', corpus)
#pprint(doctexts)
