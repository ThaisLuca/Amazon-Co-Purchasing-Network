
from graph_tool.all import *
import gc

def create_graph(network, data):
	RATING = 'Rating'
	GROUP = 'Group'
	CATEGORIES = 'Categories'

	print("Creating graph...")
	g = Graph(directed=False)

	#Adding properties
	vprop_rating = g.new_vertex_property("int")
	g.vp.rating = vprop_rating

	vprop_categories = g.new_vertex_property("int")
	g.vp.categories = vprop_categories

	vprop_group = g.new_vertex_property("object")
	g.vp.group = vprop_group


	g.add_vertex(548552)
	for line in network:
		try:
			from_node = line[0]
			to_node = line[1]

			v1 = g.vertex(from_node)
			v2 = g.vertex(to_node)


			#Set properties
			g.vp.rating[v1] = data[from_node][RATING]
			g.vp.group[v1] = data[from_node][GROUP]
			g.vp.categories[v1] = data[from_node][CATEGORIES]

			g.vp.rating[v2] = data[to_node][RATING]
			g.vp.group[v2] = data[to_node][GROUP]
			g.vp.categories[v2] = data[to_node][CATEGORIES]

			e = g.add_edge(v1,v2)
		except:
			print("Couldn't create vertices ", from_node, to_node)

	del data
	del network
	gc.collect()

	print("Graph successfully created.")
	print("  It contains %d vertices and %d edges." % (g.num_vertices(), g.num_edges()))
	return g

def save_graph(g):
	g.save('resources/amazon-ungraph.gml')
	print("Graph saved in 'resources' folder in file 'amazon-ungraph.gml'.")

def load_graph_from_file(filename):
	print("Loading graph from file..")
	return load_graph(filename)
