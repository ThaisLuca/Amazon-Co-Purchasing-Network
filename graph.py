
from graph_tool.all import *
import gc

def create_graph(file_1, file_2, similarities):
	SIMILAR = 'Similar'
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

	eprop_weight = g.new_edge_property("int")
	g.ep.weight = eprop_weight

	data = {}
	s = open(file_1, 'r')
	a = s.read()
	d1 = eval(a)
	s.close()
	data.update(d1)

	s = open(file_2, 'r')
	a = s.read()
	d2 = eval(a)
	s.close()
	data.update(d2)

	keys = sorted(data.items())
	g.add_vertex(548552)
	for key in keys:
		try:
			d = key[1]
			v = g.vertex(key[0])

			#Set properties
			g.vp.rating[v] = d[RATING]
			g.vp.group[v] = d[GROUP]
			g.vp.categories[v] = d[CATEGORIES]
		except:
			print("Couldn't create vertice ", key[0])

	del data
	gc.collect()

	sim = open(similarities, 'r').read()
	sim = eval(sim)

	for key in sim:
		from_node = key[0]
		to_node = key[1]

		try:
			v1 = g.vertex(from_node)
			v2 = g.vertex(to_node)

			e = g.add_edge(v1, v2)
			d.ep.weight[e] = sim[key]
			#print("Added vertices %d and %d with weight %d" %(from_node, to_node, sim[key]))
		except:
			print("Couldn't find nodes %d and %d" % (from_node, to_node))

	del sim
	gc.collect()

	print("Graph successfully created.")
	print("  It contains %d vertices and %d edges." % (g.num_vertices(), g.num_edges()))
	return g

def save_graph(g):
	g.save('amazon-ungraph.gml')

def load_graph_from_file():
	print("Loading graph from file..")
	return load_graph('resources/amazon-ungraph.gml')
