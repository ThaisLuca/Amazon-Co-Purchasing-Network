from __future__ import division

import csv
import os, sys

# Loads network file into a matrix
def load_file(filename):
	print("Reading file...")
	data = []
	ignored_lines = 0
	with open(filename) as f:
		for line in f:
			if ignored_lines < 4:
				ignored_lines += 1
			else:
				node = line.split()
				data.append([node[0], node[1]])
			if(len(data)*2 > floor(334863/2)):
				break
	print("Reading completed.")
	print(len(data)*2)
	f.close()
	return data


def load_metadata_file(filename):
	print("Reading meta data file...")
	data = {}
	salesrank=group=categories=rating=similar=None
	with open(filename, encoding="utf8") as f:
		for line in f:
			line = line.split()
			try:
				for i in range(0, len(line)):
					if(line[i].startswith("Id:")):
						Id = line[i+1]
						break
					elif (line[i].startswith("group")):
						group = line[i+1]
						break
					elif(line[i].startswith("categories")):
						categories = line[i+1]
						break
					elif(line[i].startswith("avg") and line[i+1].startswith("rating")):
						rating = line[i+2]
					elif(line[i].startswith("similar")):
						similar = line[i+1:len(line)]
						break
			except:
				print("Couldn't read character in position ", i)
			if(rating):
				try:
					rating = int(rating)
				except:
					rating = float(rating)
			if(rating and rating >= 3):
				data[Id] = {'Group': group, 'Categories': categories, 'Rating': rating, 'Similar': similar}
	f.close()
	return data

def get_similar_products(data):
	data_s = {}
	for key in data:
		similars = data[key]['Similar']
		for s in similars:
			if(s[-1] == "X"): s = s[:-1]
			if(s > key): 
				tupl = (key, s)
			else: 
				tupl = (s, key)
			if(tupl in data_s):
				data_s[tupl] += 1
			else:
				data_s[tupl] = 1
	return data_s

def save_dict(dictionary, name):
	f = open(name,"w")
	f.write(str(dictionary))
	f.close()

def load_dict(filename):
	print("Loading dict...")
	s = open(filename, 'r').read()
	dt = eval(s)
	print("Dict loaded.")
	return dt
