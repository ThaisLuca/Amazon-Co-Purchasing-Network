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

data = remove_not_int_ids(load_metadata_file('amazon-meta.txt'))

# Save for later
save_dict(data, 'meta-data.txt')