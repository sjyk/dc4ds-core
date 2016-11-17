#!/usr/bin/env python
import csv
import numpy as np
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import scipy
import unicodedata

#basic error handling
def tryParse(X):

	vals = []

	if X.shape == (1,1):
		try:
			vals.append(float(X.tolist()[0][0]))
		except ValueError:
			vals.append(0)

		return vals


	for x in np.squeeze(X.T):
		try:
			vals.append(float(x))
		except ValueError:
			vals.append(0)

	return vals

def tryParseList(Y):

	return tryParse(np.array(Y))

#converts the labeled dataset into features and labels
def featurize(features_dataset, types):
	feature_list = []
	transform_list = []
	fmap = {}
	fstart = 0

	for i,t in enumerate(types):
		col = [f[i] for f in features_dataset]

		if t == "string" or t == "categorical" or t =="address":
			vectorizer = CountVectorizer(min_df=1, token_pattern='\S+')
			vectorizer.fit(col)
			feature_list.append(vectorizer.transform(col))
			transform_list.append(vectorizer)

			fprev = fstart
			fstart = fstart + feature_list[-1].shape[1]
			for j in range(fprev, fstart):
				fmap[j] = i

		else:
			vectorizer = FunctionTransformer(tryParse)
			vectorizer.fit(col)
			feature_list.append(scipy.sparse.csr_matrix(vectorizer.transform(col)).T)
			transform_list.append(vectorizer)

			fprev = fstart
			fstart = fstart + 1
			for j in range(fprev, fstart):
				fmap[j] = i

	features = scipy.sparse.hstack(feature_list).tocsr()
	return features, transform_list, fmap

#converts the labeled dataset into features and labels
def featurizeFromList(features_dataset, types, tlist):
	feature_list = []
	transform_list = []

	for i,t in enumerate(types):
		col = [f[i] for f in features_dataset]

		if t == "string" or t == "categorical" or t =="address":
			vectorizer = tlist[i]
			feature_list.append(vectorizer.transform(col))
		else:
			vectorizer = tlist[i]
			#print scipy.sparse.csr_matrix(vectorizer.transform(col)).T
			feature_list.append(scipy.sparse.csr_matrix(vectorizer.transform(col)).T)

	features = scipy.sparse.hstack(feature_list).tocsr()
	return features

def get_acc_scores(ytrue, ypred, yscores=None):
	
	if yscores == None:
		yscores = ypred
	
	return [accuracy_score(ytrue, ypred), f1_score(ytrue, ypred), roc_auc_score(ytrue, yscores, 'weighted')]


#converts a label column into a vector
def labelize(column, t):

	if t == "string":
		raise ValueError("String valued labels are not supported")
	elif t == "categorical":

		label_map = {} 
		for i,k in enumerate(set(column)):
			label_map[k] = i

		vectorizer = FunctionTransformer(lambda x: label_map[x[0,0]])

		return vectorizer.fit_transform(column), vectorizer

	else:

		vectorizer = FunctionTransformer(tryParse)
		
		return vectorizer.fit_transform(column), vectorizer





