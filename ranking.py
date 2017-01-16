import json
import operator
import numpy as np 
from math import sqrt,log
from gensim import corpora, models, similarities
from gensim.models.ldamodel import LdaModel
from collections import defaultdict
from pprint import pprint
import sys
import glob, os

##########################################################################################
###################		RANKING USING LDA AND HEATMAPS 	##################################
##########################################################################################

def topic_difficulty_lda_heatmaps(heatmap_json, lda_pi_json):
	with open(heatmap_json) as json_heatmap:
		heatmap = json.load(json_heatmap)
	
	with open(lda_pi_json) as json_lda_pi:
		lda_pi = json.load(json_lda_pi)
	
	topic_prob = {}

	for lecture in heatmap:
		minutes1 = heatmap[lecture]
		minutes2 = lda_pi[lecture]

		if len(minutes1)!= len(minutes2):
			print "lecture: ",lecture, "doesn't match!", " lda_pi: ", len(minutes2), " heat: ", len(minutes1)
		for minute in range(min(len(minutes1),len(minutes2))):
			for topic_dist in lda_pi[lecture][minute]:
				topic = topic_dist[0]
				if topic not in topic_prob:
					topic_prob[topic] = {'numerator_sum': 0, 'pi_sum':0, 'heat_sum':0}
				topic_prob[topic]['numerator_sum']+= heatmap[lecture][minute]*topic_dist[1]
				topic_prob[topic]['pi_sum']+=topic_dist[1]**2
				topic_prob[topic]['heat_sum']+= heatmap[lecture][minute]**2
	
	topic_difficulties={}
	for t in topic_prob:
		topic_difficulties[t] = float(topic_prob[t]['numerator_sum'])/float(sqrt(topic_prob[t]['heat_sum'])*sqrt(topic_prob[t]['pi_sum']))
	
	with open('heatmaps_lda_topic_ranking.json','w') as f:
		json.dump(topic_difficulties, f, sort_keys=True, indent=4)
	return

##########################################################################################
###################		RANKING USING PLSA AND HEATMAPS	##################################
##########################################################################################

def topic_difficulty_plsa_heatmaps(heatmap_json, plsa_pi_npy):
	
		with open(heatmap_json) as json_heatmap:
			heatmap = json.load(json_heatmap)
		sorted_heatmap = sorted(heatmap.items(),key=operator.itemgetter(0))
		heatmap_np = np.array([y[1] for y in sorted_heatmap])
		flatheatmap = []
		for lec in heatmap_np:
			flatheatmap.extend(lec)
		plsa_pi_np = np.load(plsa_pi_npy)

		numerator_sum = 0
		pi_sum = 0
		heat_sum = 0
		num_topics = len(plsa_pi_np[0])
		topic_prob = {}

		for t in range(num_topics):
			for doc in range(len(plsa_pi_np)):
				numerator_sum+= flatheatmap[doc]*plsa_pi_np[doc][t]
				pi_sum+=plsa_pi_np[doc][t]**2
				heat_sum+= flatheatmap[doc]**2

			topic_prob[t] = float(numerator_sum)/float(sqrt(heat_sum)*sqrt(pi_sum))
		sorted_topic_prob = sorted(topic_prob.items(),key=operator.itemgetter(1))

		with open('heatmaps_plsa_topic_ranking.json','w') as f:
			json.dump(topic_prob, f, sort_keys=True, indent=4)
		return

##########################################################################################
###################		RANKING USING LDA AND STUDENT VOTES		##########################
##########################################################################################

def topic_difficulty_lda_studentvotes(student_votes, lda_model):
	mymodel = LdaModel.load(lda_model)
	dictionary = mymodel.id2word
	sv = open(student_votes, 'r')
	student_query_bow = dictionary.doc2bow(sv.read().split())
	topics = mymodel.get_document_topics(student_query_bow)
	
	topic_difficulties = {}
	for t in range(17):
		topic_difficulties[t] = 0.0
	for tup in topics:
		topic_number = tup[0]
		prob = tup[1]
		topic_difficulties[topic_number] = prob
	with open('studentvotes_lda_topic_ranking.json','w') as f:
		json.dump(topic_difficulties, f, sort_keys=True, indent=4)
	return


##########################################################################################
###################		RANKING USING PLSA AND STUDENT VOTES	##########################
##########################################################################################

def topic_difficulty_plsa_studentvotes(student_votes, plsa_theta_npy, vocabulary_npy):
	vocabulary = np.load(vocabulary_npy)
	pprint(vocabulary)
	theta = np.load(plsa_theta_npy)
	sv = open(student_votes, 'r')
	sv_query = sv.read().split()
	query_word_freq = {}
	for w in sv_query:
		if w not in query_word_freq:
			query_word_freq[w] = 1
		else:
			query_word_freq[w]+=1

	num_topics = len(theta)
	topic_prob = {}

	for t in range(num_topics):
		p = 1.0
		for w in query_word_freq:
			if w in vocabulary:
				w_indx = np.where(vocabulary==w)
				# print w_indx[0][0]
				word_prob = theta[t][w_indx[0][0]]
				if word_prob>0:
					word_freq = query_word_freq[w]
					p += log(word_prob)*word_freq
		topic_prob[t] = p
	with open('studentvotes_plsa_topic_ranking.json','w') as f:
		json.dump(topic_prob, f, sort_keys=True, indent=4)
	return




##########################################################################################
################	CALCULATE TOPIC RANKINGS FOR ALL TOPICS IN MODEL 	##################
##########################################################################################

if (__name__ == "__main__"):
	if sys.argv[1] == 'lda_heatmaps':
		topic_difficulty_lda_heatmaps(sys.argv[2],sys.argv[3])
	elif sys.argv[1] == 'plsa_heatmaps':
		topic_difficulty_plsa_heatmaps(sys.argv[2],sys.argv[3])
	elif sys.argv[1] == 'lda_studentvotes':
		topic_difficulty_lda_studentvotes(sys.argv[2],sys.argv[3])
	elif sys.argv[1] == 'plsa_studentvotes':
		topic_difficulty_plsa_studentvotes(sys.argv[2],sys.argv[3], sys.argv[4])
	else:
		print "Arguments do not match a choice!"