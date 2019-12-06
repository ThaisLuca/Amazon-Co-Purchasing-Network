
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
	vprop_categories = g.new_vertex_property("int")
	vprop_group = g.new_vertex_property("object")
	eprop_weight = g.new_edge_property("int")

	for f in [file_1, file_2]:

		s = open(f, 'r')
		a = s.read()
		data = eval(a)

		for key in data:
			print(key)
			v = g.add_vertex()
			print(g.vertex_index[v])

			return

			#Set properties
			vprop_rating[v] = data[key][RATING]
			vprop_group[v] = data[key][GROUP]
			vprop_categories[v] = data[key][CATEGORIES]

		s.close()
		del data
		gc.collect()

	sim = open(similarities, 'r').read()
	sim = eval(sim)

	for key in sim:
		from_node = key[0]
		to_node = key[1]

		v1 = g.vertex(from_node)
		v2 = g.vertex(to_node)

		e = g.add_edge(v1, v2)
		eprop_weight[e] = sim[key]
		print("Adicionados vertices %d e %d com peso %d" %(from_node, to_node, sim[key]))

	del sim
	gc.collect()
			

#	for line in data:
#		g.add_vertex(2)
#		if line[0] not in meta or line[1] not in meta:
#			print("Passei")
#			continue

#		from_node = int(line[0])
#		to_node = int(line[1])
#		v1 = g.vertex(from_node)
#		v2 = g.vertex(to_node)

#		meta_v1 = meta[line[0]]
#		meta_v2 = meta[line[1]]

#		vprop_rating[v1] = meta_v1['Rating']
#		vprop_group[v1] = meta_v1['Group']
#		vprop_categories[v1] = meta_v1['Categories']

#		vprop_rating[v2] = meta_v2['Rating']
#		vprop_group[v2] = meta_v2['Group']
#		vprop_categories[v2] = meta_v2['Categories']

#		e = g.add_edge(v1, v2)
#		print("Adicionados vertices %d e %d" %(from_node, to_node))

	print("Graph successfully created.")
	return g

def save_graph(g):
	g.save('amazon-ungraph.gml')

def load_graph_from_file():
	print("Loading graph from file..")
	return load_graph('resources/amazon-ungraph.gml')
