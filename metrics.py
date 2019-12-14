
from __future__ import division
from graph_tool.all import *
from collections import defaultdict

def precision_and_recall(recommended, relevants):
	relevants_and_recommended = 0

	if len(relevants) == 0:
		return 0, 0

	for r in recommended:
		if r in relevants:
			relevants_and_recommended += 1

	precision = relevants_and_recommended/len(recommended)
	recall = relevants_and_recommended/len(relevants)

	return precision, recall
