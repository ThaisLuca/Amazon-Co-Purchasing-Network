from __future__ import division
from graph_tool.all import *
from scipy.stats.stats import pearsonr
from operator import itemgetter
from collections import OrderedDict
import math

ADAMIC_ADAR_SIMILARITY = "inv-log-weight"

# product is the vertex ID being seen by the user
# n is the number of products to rank for recommendation
def recommend(g, p_id, groups, N, rating_based=False):

	p_n_ids = []
	for n in g.vertices():
		_id = g.vertex_index[n]
		p_n_ids.append(_id)
	pairs = build_pairs(p_id, p_n_ids)

	# Ranking using Adamic-Adar Similarity
	adamic_adar_similarities = vertex_similarity(g, vertex_pairs=pairs, sim_type=ADAMIC_ADAR_SIMILARITY)

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = adamic_adar_similarities[i]
	
	print("\n")
	#Sort rank
	print("Ranking using Adamic-Adar Similarity\n")
	adamic_adar_recommended = print_rank(ranking, N, True)
	print("\n")

	#Ranking using Cosine Similarity
	cosine_similarities, preferencial_similarities, hub_similarities = cossine_vertex_similarity(g, p_id, vertex_pairs=pairs)

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = cosine_similarities[i]
	
	#Sort rank
	print("Ranking using Cossine Similarity\n")
	cosine_recommended = print_rank(ranking, N, True)
	print("\n")	

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = preferencial_similarities[i]

	#Sort rank
	print("Ranking using Preferencial Attachment Index\n")
	preferencial_recommended = print_rank(ranking, N, True)
	print("\n")

	#Ranking using Jaccard Similarity
	jaccard_similarities = vertex_similarity(g, vertex_pairs=pairs)

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = jaccard_similarities[i]
	
	#Sort rank
	print("Ranking using Jaccard Similarity\n")
	jaccard_recommended = print_rank(ranking, N, True)
	print("\n")

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = hub_similarities[i]
	
	#Sort rank
	print("Ranking using Hub Depressed Index\n")
	hub_recommended = print_rank(ranking, N, True)
	print("\n")

	#if(rating_based):
	#	pearson_correlations

	return adamic_adar_recommended, cosine_recommended, jaccard_recommended, preferencial_recommended, hub_recommended

def build_pairs(prod, vertices):
	pairs = []
	for n in vertices:
		pairs.append((prod, n))
	return pairs


def rank(d, N):
	rank = {}
	ids = []
	sorted_values = sorted(d, key=d.get, reverse=True)
	for r in sorted_values:
		rank[r] = d[r]
		ids.append(r[1])
	return rank, ids

def print_rank(d, N, _print=False):
	rank = {}
	ids = []
	i = 0
	sorted_values = sorted(d, key=d.get, reverse=True)
	for r in sorted_values:
		if(_print):
			print(r, d[r])
		ids.append(r[1])
		i += 1
		if i > N:
			break
	return ids

def get_rating(rating):
	try:
		r = int(rating)
	except:
		r = float(rating)
	return r

def group_convertion(group):
	string_to_int = {'Book': 100, 'Music': 200, 'DVD': 300, 'Video': 400, 'Toy': 500, 'Software': 600, 'Baby': 700, 'CE': 800, 'Sports': 900}
	return string_to_int[group]

def pearson_correlation(pairs, data):
	correlations = {}
	GROUP = 'Group'
	RATING = 'Rating'
	CATEGORIES = 'Categories'
	x = y =[1,1,1]
	
	for pair in pairs:
		try:
			rating_1 = get_rating(data[str(pair[0])][RATING])
			rating_2 = get_rating(data[str(pair[1])][RATING])

			group_1 = group_convertion(data[str(pair[0])][GROUP])
			group_2 = group_convertion(data[str(pair[1])][GROUP])

			x = [rating_1, group_1, int(data[str(pair[0])][CATEGORIES])]
			y = [rating_2, group_2, int(data[str(pair[1])][CATEGORIES])]
			p = pearsonr(x,y)
			correlations[pair] = p
		except:
			correlations[pair] = 0
	return correlations

def cossine_vertex_similarity(g, p_id, vertex_pairs):
	cossine_similarity = []
	preferencial_attachment_index = []
	hub = []

	# Computation for product id
	x_ids = []
	x = g.vertex(p_id)
	x_neighbors = x.out_neighbors()

	dx = 0
	for n in x_neighbors:
		dx += 1
		x_ids.append(g.vertex_index[n])
		
	for pair in vertex_pairs:
		
		y_ids = []
		y = g.vertex(pair[1])
		y_neighbors = y.out_neighbors()

		dy = 0
		for n in y_neighbors:
			dy+=1
			y_ids.append(g.vertex_index[n])			

		neighbors_in_common = []

		for t in x_ids:
			if t in y_ids:
				neighbors_in_common.append(t)

		if(dx > 0 and dy > 0 and max(dx,dy) > 0):
			z = math.sqrt(dx)*math.sqrt(dy)
			cossine_similarity.append(len(neighbors_in_common)/z)
			preferencial_attachment_index.append(dx*dy)
			hub.append(len(neighbors_in_common)/max(dx,dy))
		else:
			cossine_similarity.append(0)
			preferencial_attachment_index.append(0)
			hub.append(0)

	return cossine_similarity, preferencial_attachment_index, hub
			






