from graph_tool.all import *
import data as dt
import graph as gt
import pandas as pd
import plot as plt
import gc

UNGRAPH_AMAZON_NETWORK = 'resources/com-amazon.ungraph.txt'
METADATA_NETORK = 'resources/amazon-meta.txt'

gc.collect()

g, vertex_with_vertex = gt.create_graph(dt.load_file(UNGRAPH_AMAZON_NETWORK))
g = gt.remove_artificial_vertex(vertex_with_vertex, g)
gt.save_graph(g)
#g = gt.load_graph_from_file()



# print("Load graph")

# d = 0

# vertices = g.vertices()
# if d == 1:
# 	degrees = []

# 	#Find most popular vertex by its degree
# 	most_popular = None
# 	max_degree = 0
# 	sum_degrees = 0

# 	for v in vertices:
# 		d = v.out_degree()
# 		sum_degrees += d 
# 		degrees.append(d)
# 		if d > max_degree:
# 			max_degree = d 
# 			most_popular = v

# 	print("Most popular item is %d with degree %d" % (most_popular, max_degree))
# 	print("Average degree is %d" % (sum_degrees/g.num_vertices()))
# 	#plt.plot_distribution(g.num_vertices(), degrees, "Graus", 'degrees')
# 	plt.plot_ccdf(g.num_vertices(), degrees, "Graus", 'degrees')

# c = global_clustering(g)
# print("Global Clustering: %f DP: %f " % (c[0], c[1]))
# print("\n")

# gc.collect()
