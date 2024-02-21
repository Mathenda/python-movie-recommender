# Movie Rating System

This project is a simple movie rating system. It uses user-user collaborative filtering to generate predictions and uses a CSV file as a database to store movie information and user ratings.

## Dataset

The dataset used in this project is `new_file.csv`, which contains the following columns:

- `item`: The ID of the movie.
- `title`: The title of the movie.
- `genres`: The genres of the movie, separated by '|'.
- `ratings`: The user's rating of the movie.

Here's an example of the data:

```csv
item,title,genres,ratings
356,Forrest Gump (1994),Comedy|Drama|Romance|War,4
318,"Shawshank Redemption, The (1994)",Crime|Drama,4.5
296,Pulp Fiction (1994),Comedy|Crime|Drama|Thriller,4
```
## Usage
To use this project, run the main.py script. The script will randomly select a movie from the CSV file and ask you to rate it. Enter a rating between 0.0 and 5.0, or enter 'done' to finish. Your ratings will be saved back to the CSV file.

## Requirements
This project requires Python 3 and the csv and random modules, which are included in the standard Python library.

## Future Work
Future improvements to this project could include:
- Implementing a recommendation system based on the user's ratings.
- Allowing the user to add new movies to the database.
- Adding error handling for invalid inputs.

