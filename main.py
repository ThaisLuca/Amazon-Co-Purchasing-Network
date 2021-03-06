
from __future__ import division
from graph_tool.all import *
import data as dt
import graph as gt
import plot as plt
import metrics as m
import recommendation as rc
import gc, os
import numpy as np

# File paths
AMAZON_META = 'resources/amazon-meta.txt'
UNGRAPH_AMAZON_NETWORK = 'resources/amazon-ungraph.gml'
METADATA_NETWORK_1 = 'resources/meta-data_1.txt'
METADATA_NETWORK_2 = 'resources/meta-data_2.txt'
NETWORK_FILE = 'resources/com-amazon.ungraph.txt'
GROUPS_FILE = 'resources/products_groups_by_id.txt'

with_properties = False
N = 5

gc.collect()

#Pre-processing for meta-data file
# Check if dictionary of product already exists
if not os.path.isfile(METADATA_NETWORK_1) and not os.path.isfile(METADATA_NETWORK_2):
	print("Metadata files not found")

	# Build dictionary containing products description like category, average rating, categories and group. Indexed by its ID.
	# Some IDs already integer numbers, as graph-tool only accepts integer, we must remove them.
	data = dt.remove_not_int_ids(dt.load_metadata_file(AMAZON_META))

	# Save for later
	dt.save_dict(data, METADATA_NETWORK)

if os.path.isfile(METADATA_NETWORK_1) and os.path.isfile(METADATA_NETWORK_2) and os.path.isfile(NETWORK_FILE):
	print("Metadata files found")

	# Check if ungraph file exists
	if not os.path.isfile(UNGRAPH_AMAZON_NETWORK):

		print("Graph file not found")

		network = dt.load_file(NETWORK_FILE)
		if(with_properties):

			data = {}
			s = open(METADATA_NETWORK_1, 'r')
			a = s.read()
			d1 = eval(a)
			s.close()
			data.update(d1)

			s = open(METADATA_NETWORK_2, 'r')
			a = s.read()
			d2 = eval(a)
			s.close()
			data.update(d2)
			del d1
			del d2
			gc.collect()

			# Build network
			g = gt.create_graph(network, data)
		else:
			# Build network
			g = gt.create_graph(network, [])

		# Save for later
		gt.save_graph(g)

	else:

		print("Graph file found")

		g = gt.load_graph_from_file(UNGRAPH_AMAZON_NETWORK)
		print("Graph is ready to go.")
		print("  It contains %d vertices and %d edges" % (g.num_vertices(), g.num_edges()))


d = 1
if d == 1:

	print("Density: %3f" % (2*g.num_edges()/(g.num_vertices()*g.num_vertices()-g.num_vertices())))

	degrees = []

	#Find most popular vertex by its degree
	most_popular = None
	max_degree = 0
	sum_degrees = 0
	vertices = g.vertices()

	p = {}

	for v in vertices:
		d = v.out_degree()
		if d > 0:
			sum_degrees += d 
			degrees.append(d)
		if d > max_degree:
			max_degree = d 
			most_popular = v	

	print("Most popular item is %d with degree %d" % (most_popular, max_degree))
	print("Average degree is %d" % (sum_degrees/g.num_vertices()))
	plt.plot_ccdf(g.num_vertices(), degrees, "Graus", 'degrees')
	
	del degrees
	gc.collect()

	c = global_clustering(g)
	print("Global Clustering: %f DP: %f " % (c[0], c[1]))

else:	
	s = open(GROUPS_FILE, 'r')
	a = s.read()
	groups = eval(a)
	s.close()

	product_id = input('Enter a product ID ')
	vertice = g.vertex(product_id)

	relevants = []
	relevant = vertice.out_neighbors()
	for n in relevant:
		relevants.append(g.vertex_index[n])

	r_adamic_adar, r_cosine, r_jaccard, r_preferencial, r_hub = rc.recommend(g, product_id, groups, N)

	print("Precision: %3f and Recall %3f for Adamic-Adar Similarity" % m.precision_and_recall(r_adamic_adar[1:], relevants))
	print("Precision: %3f and Recall %3f for Cosine Similarity" % m.precision_and_recall(r_cosine[1:], relevants))
	print("Precision: %3f and Recall %3f for Jaccard Similarity" % m.precision_and_recall(r_jaccard[1:], relevants))
	print("Precision: %3f and Recall %3f for Preferencial Attachment Index" % m.precision_and_recall(r_preferencial[1:], relevants))
	print("Precision: %3f and Recall %3f for Hub Depressed Index" % m.precision_and_recall(r_hub[1:], relevants))



