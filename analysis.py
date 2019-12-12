
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
index = np.arange(5)
plt.bar(index, [ratings['rating_1'], ratings['rating_2'], ratings['rating_3'], ratings['rating_4'], ratings['rating_5']])
plt.xlabel('Rating', fontsize=5)
plt.ylabel('No of ratings', fontsize=5)
plt.xticks(index, label, fontsize=5, rotation=30)
plt.title('Distribuição das Avalições de Produtos')
plt.show()