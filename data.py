from __future__ import division

import os, sys

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
					elif (line[i].startswith("categories")):
						categories = line[i+1]
						break
					elif(line[i].startswith("avg") and line[i+1].startswith("rating")):
						rating = line[i+2]
					elif(line[i].startswith("similar")):
						similar = []
						_similar = line[i+1:len(line)]
						for s in _similar:
							try:
								s = int(s)
								similar.append(s)
							except:
								print("Couldn't cast ", s)
						break
			except:
				print("Couldn't read character in position ", i)
			if(rating):
				try:
					rating = int(rating)
				except:
					rating = float(rating)
			if(rating and rating >= 3):
				data[Id] = {'Group': group, 'Rating': rating, 'Similar': similar, 'Categories': categories}
	f.close()
	return data

def get_similar_products(data):
	data_s = {}
	keys = data.keys()
	for key in data:
		similars = data[key]['Similar']
		for s in similars:
			if(s[-1] == "X"): s = s[:-1]
			if(s == '0'): continue
			if(s not in keys): continue
			try:
				key = int(key)
				s = s.strip()
				s = int(s)
				if(s > key): 
					tupl = (key, s)
				else: 
					tupl = (s, key)
				if(tupl in data_s):
					data_s[tupl] += 1
				else:
					data_s[tupl] = 1
			except:
				print("Couldn't cast id ", s)
	return data_s

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
	print("Reading completed.")
	f.close()
	return data

def remove_not_int_ids(data):
	delete = []
	for key in data:
		try:
			key = int(key)
		except:
			print("Couldn't cast item ", key)
			delete.append(key)

	for key in delete:
		del data[key]
	return data

def save_dict(d):
	d1 = dict(list(d.items())[len(d)//2:])
	d2 = dict(list(d.items())[:len(d)//2])

	f = open("meta-data_1.txt","w")
	f.write(str(d1))
	f.close()

	f = open("meta-data_2.txt","w")
	f.write(str(d2))
	f.close()

def load_dict(filename):
	print("Loading dict...")
	s = open(filename, 'r').read()
	dt = eval(s)
	print("Dict loaded.")
	return dt
