
#-*- coding: utf-8 -*-

from __future__ import division
from graph_tool.all import *
import data as dt
import graph as gt
import plot as plt
import metrics as m
import recommendation as rc
import gc, os

UNGRAPH_AMAZON_NETWORK = 'resources/amazon-ungraph.gml'
METADATA_NETWORK_1 = 'resources/meta-data_1.txt'
METADATA_NETWORK_2 = 'resources/meta-data_2.txt'

g = gt.load_graph_from_file(UNGRAPH_AMAZON_NETWORK)
print("Graph is ready to go.")
print("  It contains %d vertices and %d edges" % (g.num_vertices(), g.num_edges()))

N_precision_adamic_adar = []
N_precision_cosine = []
N_precision_jaccard = []
N_precision_PA = []
N_precision_hub = []

N_recall_adamic_adar = []
N_recall_cosine = []
N_recall_jaccard = []
N_recall_PA = []
N_recall_hub = []

degrees = [1, 10, 142, 20, 151, 160, 549, 40, 171, 50, 180, 60, 324, 70, 205, 80, 90, 219, 100, 230, 120]

p_ids = [12, 92, 110214, 21, 38365, 194384, 548091, 4711, 21209, 8975, 399944, 74484, 458358, 54379, 239107, 164581, 28211, 291117, 3250, 199628, 119157]


N = [1,5,10,20]
current = 1

sim_adamic_adar = {}
sim_cosine = {}
sim_jaccard = {}
sim_PA = {}
sim_hub = {}

for n_rank in N:
	print("N ", n_rank)
	for p_id in p_ids:

		print(current, p_id)
		current+=1
	
		vertice = g.vertex(p_id)

		relevants = []
		relevant = vertice.out_neighbors()
		
		for n in relevant:
			relevants.append(g.vertex_index[n])

		degree = len(relevants)

		
		properties_based = False

		if(properties_based):
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

			correlations = rc.pearson_correlation(pairs, data)

		if(p_id not in sim_adamic_adar):
			print("Não achou")

			p_n_ids = []
			for n in g.vertices():
				_id = g.vertex_index[n]
				p_n_ids.append(_id)
			pairs = rc.build_pairs(p_id, p_n_ids)
	
			adamic_adar_similarities = vertex_similarity(g, vertex_pairs=pairs, sim_type="inv-log-weight")
			cosine_similarities, preferencial_similarities, hub_similarities = rc.cossine_vertex_similarity(g, p_id, vertex_pairs=pairs)
			jaccard_similarities = vertex_similarity(g, vertex_pairs=pairs)
		

			sim_adamic_adar[p_id] = adamic_adar_similarities
			sim_cosine[p_id] = cosine_similarities
			sim_jaccard[p_id] = jaccard_similarities
			sim_PA[p_id] = preferencial_similarities
			sim_hub[p_id] = hub_similarities
		else:
			print("Achou")

			adamic_adar_similarities = sim_adamic_adar[p_id]
			cosine_similarities = sim_cosine[p_id]
 			preferencial_similarities = sim_PA[p_id]
			hub_similarities = sim_hub[p_id]
			jaccard_similarities = sim_jaccard[p_id]

		if(properties_based):


			adamic_adar_ranking = {}
			for i in range(0, len(pairs)):
				adamic_adar_ranking[pairs[i]] = adamic_adar_similarities[i] * max(correlations[i])

			cossine_ranking = {}
			for i in range(0, len(pairs)):
				cossine_ranking[pairs[i]] = cosine_similarities[i] * max(correlations[i])

			jaccard_ranking = {}
			for i in range(0, len(pairs)):
				jaccard_ranking[pairs[i]] = jaccard_similarities[i] * max(correlations[i])

			pa_ranking = {}
			for i in range(0, len(pairs)):
				pa_ranking[pairs[i]] = preferencial_similarities[i] * max(correlations[i])

			hub_ranking = {}
			for i in range(0, len(pairs)):
				hub_ranking[pairs[i]] = hub_similarities[i] * max(correlations[i])

		else:
			adamic_adar_ranking = {}
			for i in range(0, len(pairs)):
				adamic_adar_ranking[pairs[i]] = adamic_adar_similarities[i]

			cossine_ranking = {}
			for i in range(0, len(pairs)):
				cossine_ranking[pairs[i]] = cosine_similarities[i]

			jaccard_ranking = {}
			for i in range(0, len(pairs)):
				jaccard_ranking[pairs[i]] = jaccard_similarities[i]

			pa_ranking = {}
			for i in range(0, len(pairs)):
				pa_ranking[pairs[i]] = preferencial_similarities[i]

			hub_ranking = {}
			for i in range(0, len(pairs)):
				hub_ranking[pairs[i]] = hub_similarities[i]


		print("Results for N = %d\n" % n_rank)

		adamic_adar_recommended = rc.print_rank(adamic_adar_ranking, n_rank)
		precision_adadmic_adar, recall_adamic_adar = m.precision_and_recall(adamic_adar_recommended[1:], relevants)
		N_precision_adamic_adar.append(precision_adadmic_adar)
		N_recall_adamic_adar.append(recall_adamic_adar)

		cosine_recommended = rc.print_rank(cossine_ranking, n_rank)
		precision_cosine, recall_cosine = m.precision_and_recall(cosine_recommended[1:], relevants)
		N_precision_cosine.append(precision_cosine)
		N_recall_cosine.append(recall_cosine)

		jaccard_recommended = rc.print_rank(jaccard_ranking, n_rank)
		precision_jaccard, recall_jaccard = m.precision_and_recall(jaccard_recommended[1:], relevants)
		N_precision_jaccard.append(precision_jaccard)
		N_recall_jaccard.append(recall_jaccard)

		pa_recommended = rc.print_rank(pa_ranking, n_rank)
		precision_pa, recall_pa = m.precision_and_recall(pa_recommended[1:], relevants)
		N_precision_PA.append(precision_pa)
		N_recall_PA.append(recall_pa)

		hub_recommended = rc.print_rank(hub_ranking, n_rank)
		precision_hub, recall_hub = m.precision_and_recall(hub_recommended[1:], relevants)
		N_precision_hub.append(precision_hub)
		N_recall_hub.append(recall_hub)

		print("Precision: %3f and Recall %3f for Adamic-Adar Similarity" % (precision_adadmic_adar, recall_adamic_adar))
		print("Precision: %3f and Recall %3f for Cosine Similarity" % (precision_cosine, recall_cosine))
		print("Precision: %3f and Recall %3f for Jaccard Similarity" % (precision_jaccard, recall_jaccard))
		print("Precision: %3f and Recall %3f for Preferencial Attachment Index" % (precision_pa, recall_pa))
		print("Precision: %3f and Recall %3f for Hub Depressed Index" % (precision_hub, recall_hub))

	dt.save_to_file(n_rank, N_precision_adamic_adar, N_precision_cosine, N_precision_jaccard, N_precision_PA, N_precision_hub, 'Precision')

	dt.save_to_file(n, N_recall_adamic_adar, N_recall_cosine, N_recall_jaccard, N_recall_PA, N_recall_hub, 'Recall')


	plt.plot_N_curve(N_precision_adamic_adar, N_precision_cosine, N_precision_jaccard, N_precision_PA, N_precision_hub, N, degrees, 'Precisão', "upper left")
	plt.plot_N_curve(N_recall_adamic_adar, N_recall_cosine, N_recall_jaccard, N_recall_PA, N_recall_hub, N, degrees, 'Recall', "upper left")
	
	N_precision_adamic_adar = []
	N_precision_cosine = []
	N_precision_jaccard = []
	N_precision_PA = []
	N_precision_hub = []

	N_recall_adamic_adar = []
	N_recall_cosine = []
	N_recall_jaccard = []
	N_recall_PA = []
	N_recall_hub = []

	#plt.plot_curves(N_precision_adamic_adar, N_precision_cosine, N_precision_jaccard, N_precision_PA, N_precision_hub, 'Precisão', 'Top-N Precisão', "upper right")
	#plt.plot_curves(N_recall_adamic_adar, N_recall_cosine, N_recall_jaccard, N_recall_PA, N_recall_hub, 'Recall', 'Top-N Recall', "upper left")



