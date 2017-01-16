import json
import operator
import numpy as np 
from math import sqrt,log
import sys
import glob, os
from pprint import pprint


def compareRankings(heatmaps_lda, studentvotes_lda, heatmaps_plsa, studentvotes_plsa):

	##### LDA #######
	with open(heatmaps_lda) as lda_heatmaps:
		lda_ht = json.load(lda_heatmaps)
	lda_ht_sorted = sorted(lda_ht.items(), key=operator.itemgetter(1))
	lda_ht_ranking = [t[0] for t in lda_ht_sorted]
	# print "lda_ht_ranking: ", lda_ht_ranking
	lda_ht_sets = []
	for t in range(len(lda_ht_ranking)):
		lda_ht_sets.append(set(lda_ht_ranking[:t+1]))
	# print "lda_ht_sets: ", lda_ht_sets

	with open(studentvotes_lda) as lda_studentvotes:
		lda_sv = json.load(lda_studentvotes)
	lda_sv_sorted = sorted(lda_sv.items(), key=operator.itemgetter(1))
	lda_sv_ranking = [t[0] for t in lda_sv_sorted]
	# print "lda_sv_ranking: ", lda_sv_ranking
	lda_sv_sets = []
	for t in range(len(lda_sv_ranking)):
		lda_sv_sets.append(set(lda_sv_ranking[:t+1]))
	# print "lda_sv_sets: ", lda_sv_sets


	lda_measure = 0.0
	for depth in range(len(lda_ht_sets)):
		lda_measure+= len(lda_ht_sets[depth] & lda_sv_sets[depth])/float(depth+1)
	lda_measure = lda_measure/float(len(lda_ht_ranking))
	print "lda_measure: ", lda_measure


	##### PLSA #######
	with open(heatmaps_plsa) as plsa_heatmaps:
		plsa_ht = json.load(plsa_heatmaps)
	plsa_ht_sorted = sorted(plsa_ht.items(), key=operator.itemgetter(1))
	plsa_ht_ranking = [t[0] for t in plsa_ht_sorted]
	# pprint(plsa_ht_ranking)
	plsa_ht_sets = []
	for t in range(len(plsa_ht_ranking)):
		plsa_ht_sets.append(set(plsa_ht_ranking[:t+1]))
	# pprint(plsa_ht_sets)

	with open(studentvotes_plsa) as plsa_studentvotes:
		plsa_sv = json.load(plsa_studentvotes)
	plsa_sv_sorted = sorted(plsa_sv.items(), key=operator.itemgetter(1))
	plsa_sv_ranking = [t[0] for t in plsa_sv_sorted]
	# pprint(plsa_sv_ranking)
	plsa_sv_sets = []
	for t in range(len(plsa_sv_ranking)):
		plsa_sv_sets.append(set(plsa_sv_ranking[:t+1]))
	# pprint(plsa_sv_sets)


	plsa_measure = 0.0
	for depth in range(len(plsa_ht_sets)):
		plsa_measure+= len(plsa_ht_sets[depth] & plsa_sv_sets[depth])/float(depth+1)
	plsa_measure = plsa_measure/float(len(plsa_ht_ranking))
	print "plsa_measure: ", plsa_measure




if (__name__ == "__main__"):
	compareRankings(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])