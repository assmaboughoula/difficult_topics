import urllib2
import numpy as np
import math
from sets import Set
import pprint
from scipy.sparse import *
from scipy import *

print "Loading data...."

corpus = np.load('plsa_corpus.npy')
num_docs = len(corpus)
print "num_docs = ", num_docs

vocab = np.load('vocabulary.npy')
vocab_size = len(vocab)
print "vocab_size = ", vocab_size

term_doc_matrix = np.load('term_doc_matrix.npy')

prob_w_in_D = np.load('prob_w_in_D.npy')
print "prob_w_in_D.shape = ", prob_w_in_D.shape

print "Data loaded!"

def plsaEM(corpus, k, lmda, lmdak, randSeed, max_iter):

	#initialize distributions
	
	theta_matrix = np.random.random(size=(k,vocab_size))
	for t in range(k):
		theta_matrix[t] = normalize(theta_matrix[t])

	pi_matrix = np.random.random(size=(num_docs,k))
	for d in range(num_docs):
		pi_matrix[d] = normalize(pi_matrix[d])

	p_theta = np.random.random(k) # vector of p(theta_i)
	p_theta = normalize(p_theta)


	likelihoods = []
	deltas = []
	diff = 1
	
	for iteration in range(max_iter):
		print "Iteration: ", iteration
		z_d = np.zeros((num_docs,k),dtype=np.longfloat)  #p(z|d)
		z0_d = np.zeros((num_docs),dtype=np.longfloat) #p(z=0|d)
		p_d_background = np.ones((num_docs),dtype=np.longfloat)
		p_d_k = np.ones((num_docs, k),dtype=np.longfloat)


		print "E-step:"
		for d in range(num_docs): # over all docs
			z0_d_denom = 0.0
			for t in range(k):
				for w in np.nonzero(term_doc_matrix[d])[0]: # over all words in doc d
					count = term_doc_matrix[d][w]
					p_d_k[d][t] *= (lmdak*prob_w_in_D[w]+(1-lmdak)*theta_matrix[t][w])**count
					p_d_background[d] *= math.pow(prob_w_in_D[w],count)
				z0_d_denom+=pi_matrix[d][t]*p_d_k[d][t]
				z_d[d][t]=(p_theta[t]*p_d_k[d][t])
			z_d[d] = normalize(z_d[d])	
			z0_d[d] = (lmda*p_d_background[d])/(lmda*p_d_background[d]+(1-lmda)*z0_d_denom)
				
		### M-step
		print "M-step:"
		pi_matrix = np.zeros((num_docs,k))
		for d in range(num_docs):
			for w in np.nonzero(term_doc_matrix[d])[0]:
				for t in range(k):
					pi_matrix[d][t] += term_doc_matrix[d][w] * (1-z0_d[d]) * z_d[d][t]
			pi_matrix[d] = normalize(pi_matrix[d])
		for d in range(num_docs):
			for w in np.nonzero(term_doc_matrix[d])[0]:
				for t in range(k):
					theta_matrix[t][w] = term_doc_matrix[d][w] * (1-z0_d[d]) * z_d[d][t]
		for t in range(k):
			theta_matrix[t] = normalize(theta_matrix[t])

		for t in range(k):
			p_theta[t] = sum(z_d[:,t])
		p_theta = normalize(p_theta)

		# Calculate log-likelihood and difference
		print "Updating likelihood function..."
		new_log_likelihood = 0.0 
		for d in range(num_docs):
			log = lmda*p_d_background[d]+(1-lmda)*p_theta[t]*sum(p_d_k[d])
			if log<0:
				print log
			new_log_likelihood += math.log(log)


		likelihoods.append(new_log_likelihood)
		print "updated likelihoods = ", likelihoods
		if len(likelihoods)>1:
			old_likelihood = likelihoods[len(likelihoods)-2]
			new_likelihood = likelihoods[len(likelihoods)-1]
			diff = (old_likelihood - new_likelihood)/float(old_likelihood)
			print "diff = ", diff
			deltas.append(diff)
		if diff<0.0001:
			print "Converged!"
			print "max likelihood = ", likelihoods[-1]
			break

	np.save('theta_matrix.npy', theta_matrix)
	np.save('pi_matrix.npy', pi_matrix)


def normalize(data):
    total = 0.0
    for i in range(len(data)):
        total = total + data[i]
    for i in range(len(data)):
        data[i] = data[i]/total
    return data


####################################################################################
########################### TESTING CODE. USE THIS FOR TESTING!!####################

# function signature: plsaEM(corpus, k, lmda, randSeed, max_iter)



plsaEM(corpus,17,0.9, 0.9, 0.1,100)










