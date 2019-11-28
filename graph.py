
from graph_tool.all import *

def create_graph(data):
	#data = data[:100]
	has_edge = []
	print("Creating graph...")
	g = Graph(directed=False)
	g.add_vertex(548552)
	for line in data:
		from_node = int(line[0])
		to_node = int(line[1])
		v1 = g.vertex(from_node)
		v2 = g.vertex(to_node)
		has_edge.append(v1)
		has_edge.append(v2)
		e = g.add_edge(v1, v2)
		#print("Adicionados vertices %d e %d" %(from_node, to_node))

	print("Graph successfully created.")
	return g, has_edge

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
		g.remove_vertex(v)
	print(g.num_vertices())
	return g