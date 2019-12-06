from graph_tool.all import *
import data as dt
import graph as gt
import plot as plt
import gc, os

# Files paths
AMAZON_META = 'resources/amazon-meta.txt'
UNGRAPH_AMAZON_NETWORK = 'resources/amazon-ungraph.gml'
METADATA_NETORK_1 = 'resources/meta-data_1.txt'
METADATA_NETORK_2 = 'resources/meta-data_2.txt'
SIMILARITIES = 'resources/similarities-dict.txt'

gc.collect()

#Pre-processing for meta-data file
# Check if dictionary of product already exists
if not os.path.isfile(METADATA_NETORK_1) and not os.path.isfile(METADATA_NETORK_2):
	print("Metadata files not found")

	# Build dictionary containing products description like category, average rating, categories and group. Indexed by its ID.
	# Some IDs already integer numbers, as graph-tool only accepts integer, we must remove them.
	data = dt.remove_not_int_ids(dt.load_metadata_file(AMAZON_META))

	# Save for later
	dt.save_dict(data, METADATA_NETORK)


# Check if dictionary containig relantionship between products already exists
if not os.path.isfile(SIMILARITIES):

	# Build dictionary measuring relantionship between products
	sim = dt.get_similar_products(data)

	# Save for later
	dt.save_dict(sim, SIMILARITIES)

if os.path.isfile(METADATA_NETORK_1) and os.path.isfile(METADATA_NETORK_2):
	print("Metadata files found")

	# Check if ungraph file exists
	if not os.path.isfile(UNGRAPH_AMAZON_NETWORK):

		print("Graph file not found")

		# Build network
		g = gt.create_graph(METADATA_NETORK_1, METADATA_NETORK_2, SIMILARITIES)

		# Save for later
		gt.save_graph(g)

	else:
		print("Graph file found")

		g = gt.load_graph_from_file(UNGRAPH_AMAZON_NETWORK)
		print("Graph is ready to go.")
		print("  It contains %d vertices and %d edges" % (g.num_vertices(), g.num_edges()))


d = 0

vertices = g.vertices()
if d == 1:
	degrees = []

	#Find most popular vertex by its degree
	most_popular = None
	max_degree = 0
	sum_degrees = 0

	for v in vertices:
		d = v.out_degree()
		sum_degrees += d 
		degrees.append(d)
		if d > max_degree:
			max_degree = d 
			most_popular = v

	print("Most popular item is %d with degree %d" % (most_popular, max_degree))
	print("Average degree is %d" % (sum_degrees/g.num_vertices()))
	#plt.plot_distribution(g.num_vertices(), degrees, "Graus", 'degrees')
	plt.plot_ccdf(g.num_vertices(), degrees, "Graus", 'degrees')

#c = global_clustering(g)
#print("Global Clustering: %f DP: %f " % (c[0], c[1]))
#print("\n")

#gc.collect()
