
from graph_tool.all import *
from scipy import spatial

# product is the vertex being seen by the user
# n is the number of products to rank for recommendation
def recommend(product, n, groups):
	product_neighboors = product.out_neighboors()

	product_index = g.vertex_index[product]
	product_rating = g.vp.rating[product]
	product_group = groups[product_index]
	product_categories = g.vp.categories[product]

	all_neighboors = []
	if(len(product_neighboors) < n):
		all_neighboors = all_neighboors + product_neighboors
		for v in product_neighboors:
			all_neighboors = all_neighboors + v.out_neighboors()

	sum_degrees = 0
	for n in all_neighboors:
		sum_degrees += n.out_degree()

	ranking = {}
	for n in all_neighboors:
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





