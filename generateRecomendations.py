import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv('tmdb_5000_movies.csv')

# Clean data
df = df[['title', 'genres', 'original_language', 'overview']]
df.dropna(subset=['overview', 'genres'], inplace=True)

# Convert genres JSON string into list of names
def extract_genres(g):
    try:
        genre_list = eval(g)
        return [genre['name'] for genre in genre_list]
    except:
        return []

df['genre_list'] = df['genres'].apply(extract_genres)

# Form tags = genres + overview
df['tags'] = df['genre_list'].apply(lambda x: " ".join(x)) + " " + df['overview']

# Drop duplicates
df.drop_duplicates(subset=['title'], inplace=True)

# ✅ Fix the IndexError by resetting index
df.reset_index(drop=True, inplace=True)

# Vectorize the tags
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()

# Cosine similarity matrix
similarity = cosine_similarity(vectors)

# Dictionary to store recommendations
recommendations = {}

# Loop through each movie
for index, row in df.iterrows():
    lang = row['original_language']
    genres = row['genre_list']
    title = row['title']

    for genre in genres:
        key = f"{lang}_{genre}"
        if key not in recommendations:
            recommendations[key] = {}

        # Get similar movies
        sim_scores = list(enumerate(similarity[index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:30]  # skip itself

        recs = []
        for i, score in sim_scores:
            similar_movie = df.iloc[i]
            if similar_movie['original_language'] == lang and genre in similar_movie['genre_list']:
                recs.append(similar_movie['title'])
            if len(recs) >= 10:
                break

        recommendations[key][title] = recs

print("✅ Done generating recommendations!")

# Save to JSON
with open("recommendations.json", "w", encoding="utf-8") as f:
    json.dump(recommendations, f, indent=2, ensure_ascii=False)

print("📁 Saved to recommendations.json")
