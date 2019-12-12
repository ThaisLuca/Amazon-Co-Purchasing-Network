
from graph_tool.all import *
from scipy import spatial

# product is the vertex being seen by the user
# n is the number of products to rank for recommendation
def recommend(g, product, groups):
	p_id = product
	product = g.vertex(product)
	product_neighbors = product.out_neighbors()

	p_n_ids = []
	for n in product_neighbors:
		p_n_ids.append(g.vertex_index[n])
	pairs = build_pairs(g, p_id, p_n_ids)


	# Ranking using Adamic-Adar Similarity
	adamic_adar_similarities = vertex_similarity(g, vertex_pairs=pairs, sim_type="inv-log-weight")

	ranking = {}
	for i in range(0, len(pairs)):
		ranking[pairs[i]] = adamic_adar_similarities[i]
	
	#Sort rank
	r = rank(ranking)

	return

	product_index = g.vertex_index[product]
	product_rating = g.vp.rating[product]
	product_group = groups[product_index]
	product_categories = g.vp.categories[product]

	sum_degrees = 0
	for n in all_neighboors:
		sum_degrees += n.out_degree()

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

def build_pairs(g, prod, neighbors):
	pairs = []
	for n in neighbors:
		pairs.append((prod, n))
	return pairs


def rank(d):
	v = []
	for i in sorted(d):
		print(i, d[i])
		v.append(d[i])
	return v





