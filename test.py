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

p_id = 470369
vertice = g.vertex(p_id)

relevants = []
relevant = vertice.out_neighbors()
for n in relevant:
	relevants.append(g.vertex_index[n])

p_n_ids = []
for n in g.vertices():
	_id = g.vertex_index[n]
	p_n_ids.append(_id)
pairs = rc.build_pairs(p_id, p_n_ids)

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

adamic_adar_similarities = vertex_similarity(g, vertex_pairs=pairs, sim_type="inv-log-weight")
cosine_similarities, preferencial_similarities, hub_similarities = rc.cossine_vertex_similarity(g, p_id, vertex_pairs=pairs)
jaccard_similarities = vertex_similarity(g, vertex_pairs=pairs)

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

# N = 1
print("Results for N = 1")

adamic_adar_recommended = rc.print_rank(adamic_adar_ranking, 1)
precision_adadmic_adar, recall_adamic_adar = m.precision_and_recall(adamic_adar_recommended[1:], relevants)
N_precision_adamic_adar.append(precision_adadmic_adar)
N_recall_adamic_adar.append(recall_adamic_adar)

cosine_recommended = rc.print_rank(cossine_ranking, 1)
precision_cosine, recall_cosine = m.precision_and_recall(cosine_recommended[1:], relevants)
N_precision_cosine.append(precision_cosine)
N_recall_cosine.append(recall_cosine)

jaccard_recommended = rc.print_rank(jaccard_ranking, 1)
precision_jaccard, recall_jaccard = m.precision_and_recall(jaccard_recommended[1:], relevants)
N_precision_jaccard.append(precision_jaccard)
N_recall_jaccard.append(recall_jaccard)

pa_recommended = rc.print_rank(pa_ranking, 1)
precision_pa, recall_pa = m.precision_and_recall(pa_recommended[1:], relevants)
N_precision_PA.append(precision_pa)
N_recall_PA.append(recall_pa)

hub_recommended = rc.print_rank(hub_ranking, 1)
precision_hub, recall_hub = m.precision_and_recall(hub_recommended[1:], relevants)
N_precision_hub.append(precision_hub)
N_recall_hub.append(recall_hub)

print("Precision: %3f and Recall %3f for Adamic-Adar Similarity" % (precision_adadmic_adar, recall_adamic_adar))
print("Precision: %3f and Recall %3f for Cosine Similarity" % (precision_cosine, recall_cosine))
print("Precision: %3f and Recall %3f for Jaccard Similarity" % (precision_jaccard, recall_jaccard))
print("Precision: %3f and Recall %3f for Preferencial Attachment Index" % (precision_pa, recall_pa))
print("Precision: %3f and Recall %3f for Hub Depressed Index" % (precision_hub, recall_hub))


# N = 2
print("Results for N = 2")

adamic_adar_recommended = rc.print_rank(adamic_adar_ranking, 2)
precision_adadmic_adar, recall_adamic_adar = m.precision_and_recall(adamic_adar_recommended[1:], relevants)
N_precision_adamic_adar.append(precision_adadmic_adar)
N_recall_adamic_adar.append(recall_adamic_adar)

cosine_recommended = rc.print_rank(cossine_ranking, 2)
precision_cosine, recall_cosine = m.precision_and_recall(cosine_recommended[1:], relevants)
N_precision_cosine.append(precision_cosine)
N_recall_cosine.append(recall_cosine)

jaccard_recommended = rc.print_rank(jaccard_ranking, 2)
precision_jaccard, recall_jaccard = m.precision_and_recall(jaccard_recommended[1:], relevants)
N_precision_jaccard.append(precision_jaccard)
N_recall_jaccard.append(recall_jaccard)

pa_recommended = rc.print_rank(pa_ranking, 2)
precision_pa, recall_pa = m.precision_and_recall(pa_recommended[1:], relevants)
N_precision_PA.append(precision_pa)
N_recall_PA.append(recall_pa)

hub_recommended = rc.print_rank(hub_ranking, 2)
precision_hub, recall_hub = m.precision_and_recall(hub_recommended[1:], relevants)
N_precision_hub.append(precision_hub)
N_recall_hub.append(recall_hub)

print("Precision: %3f and Recall %3f for Adamic-Adar Similarity" % (precision_adadmic_adar, recall_adamic_adar))
print("Precision: %3f and Recall %3f for Cosine Similarity" % (precision_cosine, recall_cosine))
print("Precision: %3f and Recall %3f for Jaccard Similarity" % (precision_jaccard, recall_jaccard))
print("Precision: %3f and Recall %3f for Preferencial Attachment Index" % (precision_pa, recall_pa))
print("Precision: %3f and Recall %3f for Hub Depressed Index" % (precision_hub, recall_hub))


# N = 5
print("Results for N = 5")

adamic_adar_recommended = rc.print_rank(adamic_adar_ranking, 5)
precision_adadmic_adar, recall_adamic_adar = m.precision_and_recall(adamic_adar_recommended[1:], relevants)
N_precision_adamic_adar.append(precision_adadmic_adar)
N_recall_adamic_adar.append(recall_adamic_adar)

cosine_recommended = rc.print_rank(cossine_ranking, 5)
precision_cosine, recall_cosine = m.precision_and_recall(cosine_recommended[1:], relevants)
N_precision_cosine.append(precision_cosine)
N_recall_cosine.append(recall_cosine)

jaccard_recommended = rc.print_rank(jaccard_ranking, 5)
precision_jaccard, recall_jaccard = m.precision_and_recall(jaccard_recommended[1:], relevants)
N_precision_jaccard.append(precision_jaccard)
N_recall_jaccard.append(recall_jaccard)

pa_recommended = rc.print_rank(pa_ranking, 5)
precision_pa, recall_pa = m.precision_and_recall(pa_recommended[1:], relevants)
N_precision_PA.append(precision_pa)
N_recall_PA.append(recall_pa)

hub_recommended = rc.print_rank(hub_ranking, 5)
precision_hub, recall_hub = m.precision_and_recall(hub_recommended[1:], relevants)
N_precision_hub.append(precision_hub)
N_recall_hub.append(recall_hub)

print("Precision: %3f and Recall %3f for Adamic-Adar Similarity" % (precision_adadmic_adar, recall_adamic_adar))
print("Precision: %3f and Recall %3f for Cosine Similarity" % (precision_cosine, recall_cosine))
print("Precision: %3f and Recall %3f for Jaccard Similarity" % (precision_jaccard, recall_jaccard))
print("Precision: %3f and Recall %3f for Preferencial Attachment Index" % (precision_pa, recall_pa))
print("Precision: %3f and Recall %3f for Hub Depressed Index" % (precision_hub, recall_hub))

# N = 10
print("Results for N = 10")

adamic_adar_recommended = rc.print_rank(adamic_adar_ranking, 10)
precision_adadmic_adar, recall_adamic_adar = m.precision_and_recall(adamic_adar_recommended[1:], relevants)
N_precision_adamic_adar.append(precision_adadmic_adar)
N_recall_adamic_adar.append(recall_adamic_adar)

cosine_recommended = rc.print_rank(cossine_ranking, 10)
precision_cosine, recall_cosine = m.precision_and_recall(cosine_recommended[1:], relevants)
N_precision_cosine.append(precision_cosine)
N_recall_cosine.append(recall_cosine)

jaccard_recommended = rc.print_rank(jaccard_ranking, 10)
precision_jaccard, recall_jaccard = m.precision_and_recall(jaccard_recommended[1:], relevants)
N_precision_jaccard.append(precision_jaccard)
N_recall_jaccard.append(recall_jaccard)

pa_recommended = rc.print_rank(pa_ranking, 10)
precision_pa, recall_pa = m.precision_and_recall(pa_recommended[1:], relevants)
N_precision_PA.append(precision_pa)
N_recall_PA.append(recall_pa)

hub_recommended = rc.print_rank(hub_ranking, 10)
precision_hub, recall_hub = m.precision_and_recall(hub_recommended[1:], relevants)
N_precision_hub.append(precision_hub)
N_recall_hub.append(recall_hub)

print("Precision: %3f and Recall %3f for Adamic-Adar Similarity" % (precision_adadmic_adar, recall_adamic_adar))
print("Precision: %3f and Recall %3f for Cosine Similarity" % (precision_cosine, recall_cosine))
print("Precision: %3f and Recall %3f for Jaccard Similarity" % (precision_jaccard, recall_jaccard))
print("Precision: %3f and Recall %3f for Preferencial Attachment Index" % (precision_pa, recall_pa))
print("Precision: %3f and Recall %3f for Hub Depressed Index" % (precision_hub, recall_hub))

# N = 20
print("Results for N = 20")

adamic_adar_recommended = rc.print_rank(adamic_adar_ranking, 20)
precision_adadmic_adar, recall_adamic_adar = m.precision_and_recall(adamic_adar_recommended[1:], relevants)
N_precision_adamic_adar.append(precision_adadmic_adar)
N_recall_adamic_adar.append(recall_adamic_adar)

cosine_recommended = rc.print_rank(cossine_ranking, 20)
precision_cosine, recall_cosine = m.precision_and_recall(cosine_recommended[1:], relevants)
N_precision_cosine.append(precision_cosine)
N_recall_cosine.append(recall_cosine)

jaccard_recommended = rc.print_rank(jaccard_ranking, 20)
precision_jaccard, recall_jaccard = m.precision_and_recall(jaccard_recommended[1:], relevants)
N_precision_jaccard.append(precision_jaccard)
N_recall_jaccard.append(recall_jaccard)

pa_recommended = rc.print_rank(pa_ranking, 20)
precision_pa, recall_pa = m.precision_and_recall(pa_recommended[1:], relevants)
N_precision_PA.append(precision_pa)
N_recall_PA.append(recall_pa)

hub_recommended = rc.print_rank(hub_ranking, 20)
precision_hub, recall_hub = m.precision_and_recall(hub_recommended[1:], relevants)
N_precision_hub.append(precision_hub)
N_recall_hub.append(recall_hub)

print("Precision: %3f and Recall %3f for Adamic-Adar Similarity" % (precision_adadmic_adar, recall_adamic_adar))
print("Precision: %3f and Recall %3f for Cosine Similarity" % (precision_cosine, recall_cosine))
print("Precision: %3f and Recall %3f for Jaccard Similarity" % (precision_jaccard, recall_jaccard))
print("Precision: %3f and Recall %3f for Preferencial Attachment Index" % (precision_pa, recall_pa))
print("Precision: %3f and Recall %3f for Hub Depressed Index" % (precision_hub, recall_hub))


plt.plot_curves(N_precision_adamic_adar, N_precision_cosine, N_precision_jaccard, N_precision_PA, N_precision_hub, 'Precisão', 'Top-N Precisão', "upper right")
plt.plot_curves(N_recall_adamic_adar, N_recall_cosine, N_recall_jaccard, N_recall_PA, N_recall_hub, 'Recall', 'Top-N Recall', "upper left")


