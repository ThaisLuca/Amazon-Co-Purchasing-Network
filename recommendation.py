from __future__ import division
from graph_tool.all import *
from scipy import spatial
from operator import itemgetter
from collections import OrderedDict
import math

ADAMIC_ADAR_SIMILARITY = "inv-log-weight"

# product is the vertex ID being seen by the user
# n is the number of products to rank for recommendation
def recommend(g, p_id, groups, N):

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
	print("Raking using Adamic-Adar Similarity\n")
	adamic_adar_recommended = print_rank(ranking, N)
	print("\n")

	#Ranking using Cosine Similarity
	cosine_similarities, preferencial_similarities = cossine_vertex_similarity(g, p_id, vertex_pairs=pairs)

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = cosine_similarities[i]
	
	#Sort rank
	print("Raking using Cossine Similarity\n")
	cosine_recommended = print_rank(ranking, N)
	print("\n")	

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = preferencial_similarities[i]

	#Sort rank
	print("Raking using Preferencial Attachment Index\n")
	preferencial_recommended = print_rank(ranking, N)
	print("\n")

	#Ranking using Jaccard Similarity
	jaccard_similarities = vertex_similarity(g, vertex_pairs=pairs)

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = jaccard_similarities[i]
	
	#Sort rank
	print("Raking using Jaccard Similarity\n")
	jaccard_recommended = print_rank(ranking, N)
	print("\n")

	return adamic_adar_recommended, cosine_recommended, jaccard_recommended, preferencial_recommended

	ranking = {}
	for n in product_neighboors:
		n_index = g.vertex_index[n]
		n_degree = product.out_degree()
		n_rating = g.vp.rating[n]
		n_group = groups[n_index]
		n_categories = g.vp.categories[n]

		if(n_group == product_group):
			g1 = g2 = 1
		else:
			g1 = 0
			g2 = 1

		if(n_categories == product_categories):
			c1 = c2 = 1
		else:
			c1 = 0
			c2 = 1

		ranking[n_index] = probability(n_degree, sum_degress)*(1-spatial.distance.cosine([n_rating, g1, c1], [product_rating, g2, c2]))

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

def print_rank(d, N):
	rank = {}
	ids = []
	i = 0
	sorted_values = sorted(d, key=d.get, reverse=True)
	for r in sorted_values:
		print(r, d[r])
		ids.append(r[1])
		i += 1
		if i > N:
			break
	return ids

def cossine_vertex_similarity(g, p_id, vertex_pairs):
	cossine_similarity = []
	preferencial_attachment_index = []

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

		if(dx > 0 and dy > 0):
			z = math.sqrt(dx)*math.sqrt(dy)
			cossine_similarity.append(len(neighbors_in_common)/z)
			preferencial_attachment_index.append(dx*dy)
		else:
			cossine_similarity.append(0)
			preferencial_attachment_index.append(0)

	return cossine_similarity, preferencial_attachment_index
			






