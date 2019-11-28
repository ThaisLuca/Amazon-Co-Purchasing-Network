
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plot
import math
import random as rd
import numpy as np

def plot_distribution(n_vertices, all_measure, xlabel, filename, metric='degree'):
    freq = freq_relative(n_vertices, all_measure, metric)
    plot.xscale('log')
    plot.yscale('log')
    plot.ylabel('CDF')
    plot.xlabel(xlabel)
    plot.plot(range(len(freq)), freq, 'o', clip_on=False)
    plot.savefig('graficos/'+filename+'_cdf.jpg')
    plot.clf()


def plot_ccdf(n_vertices, all_measure, xlabel, filename, metric='degree'):
    _ccdf = ccdf(n_vertices, all_measure, metric)
    plot.xscale('log')
    plot.yscale('log')
    plot.ylabel('CCDF')
    plot.xlabel(xlabel)
    plot.plot(range(len(_ccdf)), _ccdf, 'o', clip_on=False)
    plot.savefig('graficos/'+filename+'_ccdf.jpg')
    plot.clf()

    
def freq_relative(n_vertices, all_measure, metric='degree'):
    if metric == 'degree':
        degree_distribution = np.bincount(list(all_measure))
        return degree_distribution/n_vertices
    elif metric == 'distance':
        distance_distribution = np.bincount(list(all_measure))
        return distance_distribution/comb(n_vertices, 2)
    else:
        all_measure = np.array(all_measure)
        all_sum = float(all_measure.sum())
        return all_measure.cumsum(0)/all_sum  

def ccdf(n_vertices, all_measure, metric='degree'):
    return 1 - freq_relative(n_vertices, all_measure, metric)