import lenskit.datasets as ds
import pandas as pd

data = ds.MovieLens('lab4/')

print("Successfully installed dataset.")

rows_to_show = 10
minimum_to_include = 20

## writing to a new CSV without ratings appending commas
import csv
with open('lab4/jabril-movie-ratings.csv', 'r') as input_file, open('new_file.csv', 'w', newline='') as output_file:
    #create csv reader and writer objects
    reader = csv.reader(input_file)         # Create a CSV reader
    writer = csv.writer(output_file)        # Create a CSV writer
    
    first_row = True        # Create a flag to check if the row is the first row
    for row in reader:      # Loop through each row in the input file
        if first_row:       
            first_row = False       # If the row is the first row, write it to the output file
            writer.writerow(row)
        else:

            row = row[:-1]          # Remove the last field from the row

            row.append('')          # Add an empty field to the row
        # if row and row[-1] == ',':
        #     row = row[:-1]

            writer.writerow(row)        # Write the row to the output file
        


import random

import random

with open('new_file.csv', 'r') as input_file:
    reader = csv.reader(input_file)         # Create a CSV reader
    all_lines = list(reader)        # Read all lines from the file into a list

header = all_lines[0]       # Get the header from the list of movies
movies = all_lines[1:]          # Remove the header from the list of movies

# Loop until the user enters 'done'
while True:
    # Select a random movie and its index
    index = random.randrange(len(movies))       # Select a random movie index
    movie = movies[index]       # Select a random movie from its index

    # Ask the user for a rating
    rating = input(f'Please rate "{movie[1], movie[2]}" or enter "done" to finish: ')       # Ask the user for a rating

    # Check if the user entered 'done'
    if rating.lower() == 'done':        # If the user entered 'done',
        break

    if rating == '':            # If the user didn't enter anything, skip this movie
        continue


    movie[-1] = rating          # Replace the last field of the movie with the rating


    movies[index] = movie       # Update the movie in the list

with open('new_file.csv', 'w', newline='') as output_file:      # Write the header and movies back to the file
    writer = csv.writer(output_file)        # Create a CSV writer
    writer.writerow(header)     # Write the header
    writer.writerows(movies)        # Write the movies

print('Thank you for rating movies!')
#personalized ratings
# import csv

personal_rating_dict = {}

with open("new_file.csv", newline='') as csvfile:       #open the file
  ratings_reader = csv.DictReader(csvfile)      #create a csv reader object
  for row in ratings_reader:            #loop through each row in the file
            
    if ((row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6)):            #if the rating is not empty and is between 1 and 5
      personal_rating_dict.update({int(row['item']): float(row['ratings'])})        #add the rating to the dictionary
      
     
print("Rating dictionaries assembled!")
# print("Sanity check:")
# print("\tpersonal rating for 1197 (The Princess Bride) is " + str(personal_rating_dict[1197]))

#user-user collaborative filtering
from lenskit.algorithms import Recommender          #import the Recommender class
from lenskit.algorithms.user_knn import UserUser        #import the UserUser class

num_recs =  10        #number of recommendations to make


user_user = UserUser(15, min_nbrs=3)        #create a UserUser collaborative filtering algorithm with minimum (3) and maximum (15) number of neighbours to consider

algo = Recommender.adapt(user_user)         #adapt the UserUser algorithm to the Recommender class
algo.fit(data.ratings)            #fit the algorithm to the data

print("Set up a User User collaborative filtering algorithm.")

pers_recs = algo.recommend(-1, num_recs, ratings=pd.Series(personal_rating_dict))     
#get recommendations for the person, -1 is a placeholder for the user id showing it is not an existing user in the set
#10 is how many recommendations it should generate

joined_data = pers_recs.join(data.movies['genres'], on='item')       #join the recommendations with the genres of the movies
joined_data = joined_data.join(data.movies['title'], on='item')     #join the recommendations with the titles of the movies
joined_data = joined_data[joined_data.columns[2:]]      #remove the item column from the recommendations
print("\n\nRECOMMENDED FOR YOU:")        #print the recommendations
print(joined_data)          #print the recommendations