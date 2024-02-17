import lenskit.datasets as ds
import pandas as pd

data = ds.MovieLens('lab4-recommender-systems/')

print("Successfully installed dataset.")

rows_to_show = 10
#get moves rated by user 1
# joined_data = data.ratings.join(data.movies['genres'], on='item')       #join with the genres
# joined_data = joined_data.join(data.movies['title'], on='item')         #join with the title
# print(joined_data.head(rows_to_show))

minimum_to_include = 20

#get highest rated on average

# average_ratings = (data.ratings).groupby(['item']).mean()                           #group by item and get the mean
# rating_counts = (data.ratings).groupby(['item']).count()                            #group by item and get the count
# average_ratings = average_ratings.loc[rating_counts['rating'] > minimum_to_include] #filter out the ones that don't have enough ratings
# sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)    #sort by rating
# joined_data = sorted_avg_ratings.join(data.movies['genres'], on='item')       #join with the genres
# joined_data = joined_data.join(data.movies['title'], on='item')          #join with the title
# joined_data = joined_data[joined_data.columns[3:]]                      #only show the columns we want
# print("RECOMMENDED FOR ANYBODY:")
# print(joined_data.head(rows_to_show))

##get highest rated based on genre

# average_ratings = (data.ratings).groupby(['item']).mean()                               #group by item and get the mean
# rating_counts = (data.ratings).groupby(['item']).count()                                #group by item and get the count
# average_ratings = average_ratings.loc[rating_counts['rating'] > minimum_to_include]     #filter out the ones that don't have enough ratings
# average_ratings = average_ratings.join(data.movies['genres'], on='item')                #join with the genres
# average_ratings = average_ratings.loc[average_ratings['genres'].str.contains('Action')] #filter out the ones that don't have the genre we want

# sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)          #sort by rating
# joined_data = sorted_avg_ratings.join(data.movies['title'], on='item')                  #join with the title
# joined_data = joined_data[joined_data.columns[3:]]                                      #only show the columns we want
# print("RECOMMENDED FOR Action FANS:")
# print(joined_data.head(rows_to_show))

#personalized ratings
import csv

jabril_rating_dict = {}
jgb_rating_dict = {}

with open("lab4-recommender-systems/jabril-movie-ratings.csv", newline='') as csvfile:
  ratings_reader = csv.DictReader(csvfile)
  for row in ratings_reader:
    if ((row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6)):
      jabril_rating_dict.update({int(row['item']): float(row['ratings'])})
      
with open("lab4-recommender-systems/jgb-movie-ratings.csv", newline='') as csvfile:
  ratings_reader = csv.DictReader(csvfile)
  for row in ratings_reader:
    if ((row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6)):
      jgb_rating_dict.update({int(row['item']): float(row['ratings'])})
     
# print("Rating dictionaries assembled!")
# print("Sanity check:")
# print("\tJabril's rating for 1197 (The Princess Bride) is " + str(jabril_rating_dict[1197]))
# print("\tJohn-Green-Bot's rating for 1197 (The Princess Bride) is " + str(jgb_rating_dict[1197]))

#user-user collaborative filtering
from lenskit.algorithms import Recommender          #import the Recommender class
from lenskit.algorithms.user_knn import UserUser        #import the UserUser class

num_recs =  10        #number of recommendations to make


user_user = UserUser(15, min_nbrs=3)        #create a UserUser collaborative filtering algorithm with minimum (3) and maximum (15) number of neighbours to consider

algo = Recommender.adapt(user_user)         #adapt the UserUser algorithm to the Recommender class
algo.fit(data.ratings)            #fit the algorithm to the data

print("Set up a User User collaborative filtering algorithm.")

jab_recs = algo.recommend(-1, num_recs, ratings=pd.Series(jabril_rating_dict))     
#get recommendations for Jabril, -1 is a placeholder for the user id showing it is not an existing user in the set
#10 is how many recommendations it should generate

joined_data = jab_recs.join(data.movies['genres'], on='item')
joined_data = joined_data.join(data.movies['title'], on='item')
joined_data = joined_data[joined_data.columns[2:]]
print("\n\nRECOMMENDED FOR JABRIL:")
print(joined_data)

#Combine Recommendations lists
combined_rating_dict = {}
for k in jabril_rating_dict:
  if k in jgb_rating_dict:
    combined_rating_dict.update({k: float((jabril_rating_dict[k]+jgb_rating_dict[k])/2)})
  else:
    combined_rating_dict.update({k:jabril_rating_dict[k]})
for k in jgb_rating_dict:
   if k not in combined_rating_dict:
      combined_rating_dict.update({k:jgb_rating_dict[k]})
      
combined_recs = algo.recommend(-1, num_recs, ratings=pd.Series(combined_rating_dict))  #Here, -1 tells it that it's not an existing user in the set, that we're giving new ratings, while 10 is how many recommendations it should generate

joined_data = combined_recs.join(data.movies['genres'], on='item')      
joined_data = joined_data.join(data.movies['title'], on='item')
joined_data = joined_data[joined_data.columns[2:]]
print("\n\nRECOMMENDED FOR JABRIL / JOHN-GREEN-BOT HYBRID:")
print(joined_data)