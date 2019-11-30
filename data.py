
import csv
import os, sys
import pandas as pd

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
	print("Reading completed.")
	return data


def load_metadata_file(filename):
	print("Reading meta data file...")
	data = {}
	title=salesrank=categories=rating=None
	with open(filename, encoding="utf8") as f:
		for line in f:
			line = line.split()
			try:
				for i in range(0, len(line)):
					if(line[i].startswith("Id:")):
						Id = line[i+1]
						break
					elif(line[i].startswith("title")):
						title = ' '.join(line[i+1:len(line)])
						break
					elif(line[i].startswith("salesrank")):
						salesrank = line[i+1]
						break
					elif(line[i].startswith("categories")):
						categories = line[i+1]
						break
					elif(line[i].startswith("avg") and line[i+1].startswith("rating")):
						rating = line[i+2]
			except:
				print("Couldn't read character in position ", i)
			data[Id] = {'Title': title, 'Salesrank': salesrank, 'Categories': categories, 'Rating': rating}
	return data

def save_dict(dictionary):
	w = csv.writer(open("meta-data.csv", "w"))
	for key, val in dict.items():
    	w.writerow([key, val])
