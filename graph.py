
from graph_tool.all import *

def create_graph(data, meta):
	#data = data[:100]

	print("Creating graph...")
	g = Graph(directed=False)

	#Adding properties
	vprop_rating = g.new_vertex_property("rating")
	vprop_group = g.new_vertex_property("group")
	vprop_categories = g.new_vertex_property("category")

	for line in data:
		g.add_vertex(2)
		if line[0] not in meta or line[1] not in meta:
			print("Passei")
			continue

		from_node = int(line[0])
		to_node = int(line[1])
		v1 = g.vertex(from_node)
		v2 = g.vertex(to_node)

		meta_v1 = meta[line[0]]
		meta_v2 = meta[line[1]]

		vprop_rating[v1] = meta_v1['Rating']
		vprop_group[v1] = meta_v1['Group']
		vprop_categories[v1] = meta_v1['Categories']

		vprop_rating[v2] = meta_v2['Rating']
		vprop_group[v2] = meta_v2['Group']
		vprop_categories[v2] = meta_v2['Categories']

		e = g.add_edge(v1, v2)
		print("Adicionados vertices %d e %d" %(from_node, to_node))

	print("Graph successfully created.")
	return g

def save_graph(g):
	g.save('amazon-ungraph.gml')

def load_graph_from_file():
	print("Loading graph from file..")
	return load_graph('resources/amazon-ungraph.gml')

def remove_artificial_vertex(v_list, g):
	print("Removing artificial vertices...")
	vertices = g.vertices()
	print(g.num_vertices())
	r = set(vertices) - set(v_list)
	for v in r:
		try:
			g.remove_vertex(v)
		except:
			print("Vertex not found.")
	print(g.num_vertices())
	return g