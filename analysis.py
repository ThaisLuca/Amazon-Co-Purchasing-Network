
from matplotlib import pyplot as plt
import numpy as np
import data as dt
import os

AMAZON_META = 'resources/amazon-meta.txt'
CATEGORIES_FILE = 'resources/cat_count.txt'
GROUP_FILE = 'resources/groups_count.txt'
RATING_FILE = 'resources/rating_count.txt'

RATING='Rating'
GROUP = 'Group'
CATEGORIES = 'Categories'

if not os.path.isfile(CATEGORIES_FILE) and not os.path.isfile(GROUP_FILE) and not os.path.isfile(RATING_FILE):

	data = dt.load_metadata_file(AMAZON_META)

	ratings_1 = 0
	ratings_2 = 0
	ratings_3 = 0
	ratings_4 = 0
	ratings_5 = 0

	group = {}
	categories = {}

	for i in data:
		if int(data[i][RATING]) == 1:
			ratings_1 += 1
		elif int(data[i][RATING]) == 2:
			ratings_2 += 1
		elif int(data[i][RATING]) == 3:
			ratings_3 += 1
		elif int(data[i][RATING]) == 4:
			ratings_4 += 1
		elif int(data[i][RATING]) == 5:
			ratings_5 += 1

		if data[i][GROUP] not in group:
			group[data[i][GROUP]] = 1
		else:
			group[data[i][GROUP]] += 1

		if data[i][CATEGORIES] not in categories:
			categories[data[i][CATEGORIES]] = 1
		else:
			categories[data[i][CATEGORIES]] += 1

	f = open("groups_count.txt","w")
	f.write(str(group))
	f.close()

	f = open("cat_count.txt","w")
	f.write(str(categories))
	f.close()

	ratings = {'rating_1': ratings_1, 'rating_2': ratings_2, 'rating_3': ratings_3, 'rating_4': ratings_4, 'rating_5': ratings_5}

	f = open("rating_count.txt","w")
	f.write(str(ratings))
	f.close()

else:
	ratings = dt.load_dict(RATING_FILE)
	categories = dt.load_dict(CATEGORIES_FILE)
	groups = dt.load_dict(GROUP_FILE)

# Plot analysis about rating
index = [1,2,3,4,5]
plt.bar(index, [ratings['rating_1'], ratings['rating_2'], ratings['rating_3'], ratings['rating_4'], ratings['rating_5']], alpha=0.6)
plt.xlabel('Avaliação Média', fontsize=10)
plt.ylabel('Número de Avaliações', fontsize=10)
plt.xticks(index, index, fontsize=10)
plt.title('Distribuição das Avaliações dos Produtos')
plt.show()

# Plot analysis about groups
index = list(groups.keys())

numbers_1 = []
numbers_2 = []
for i in groups:
	if i not in ['Book', 'Music', 'DVD', 'Video']:
		numbers_2.append(groups[i])
	else:
		numbers_1.append(groups[i])

plt.bar(index[:4], numbers_1, alpha=0.4)
plt.ylabel('Número de Produtos por Grupo', fontsize=10)
plt.xticks([0,1,2,3], index[:4], fontsize=10)
plt.title('Distribuição dos Produtos por Grupo')
plt.show()

plt.bar(index[4:], numbers_2, alpha=0.4)
plt.ylabel('Número de Produtos por Grupo', fontsize=10)
plt.xticks([0,1,2,3], index[4:], fontsize=10)
plt.title('Distribuição dos Produtos por Grupo')
plt.show()

# Plot analysis about categories
index = list(categories.keys())
size = 30
# We have 88 different categories, so we'll plot online the first 30
numbers = []
for i in index[:size]:
	numbers.append(categories[i])


plt.bar(index[:size], numbers, alpha=0.4)
plt.xlabel('Categoria', fontsize=10)
plt.ylabel('Número de Produtos por Categoria', fontsize=10)
plt.xticks(index[:size], index[:size], fontsize=7)
plt.title('Distribuição dos Produtos por Categoria')
plt.show()