import pandas as pd
import requests
import matplotlib.pyplot as plt

api_key = "662713a6"
base_url = "http://www.omdbapi.com/"


def get_movie_data(title):
    params = {
        't': title,  
        'apikey': api_key  
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Error fetching data for {title}: {response.status_code}")
        return None



movie_titles = ["Déjà Vu", "The Equalizer", "The Equalizer 3", "The Great Debaters", "American Gangster",
                "Inside Man", "Training Day", "He Got Game", "The Book of Eli", "Unstoppable"]

movie_list = []

# Fetch data for each movie and store it in the list
for title in movie_titles:
    data = get_movie_data(title)
    if data:
        if data['imdbRating'] != 'N/A':
            rating = float(data['imdbRating'])
        else:
            rating = None

        if data['imdbVotes'] != 'N/A':
            votes = int(data['imdbVotes'].replace(",", ""))
        else:
            votes = None

        # Store movie information
        movie_info = {
            'Title': data['Title'],
            'Genre': data['Genre'],
            'Year': data['Year'],
            'Rating': rating,
            'Votes': votes
        }
        movie_list.append(movie_info)

# Convert the movie list to a DataFrame
movie_df = pd.DataFrame(movie_list)

print(movie_df)

# Split genres into a list and create a new column for each genres
movie_df['Genres'] = movie_df['Genre'].apply(lambda x: x.split(", "))

# Explode the genres list so that each genre has its own row
genre_df = movie_df.explode('Genres')

# Group by genre and calculate the average rating
genre_ratings = genre_df.groupby('Genres')['Rating'].mean().sort_values(ascending=False)

print(genre_ratings)

# Plot the average rating by genre
plt.figure(figsize=(10, 6))
genre_ratings.plot(kind='bar', color='skyblue')

plt.title('Average Movie Rating by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Rating')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

