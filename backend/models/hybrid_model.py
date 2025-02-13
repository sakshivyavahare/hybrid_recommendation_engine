import pandas as pd
import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Products and Interactions data (adjust paths as needed)
products_df = pd.read_csv("../data/large_products.csv")
interactions_df = pd.read_csv("../data/large_interactions.csv")

# -------------------------------
# Content-Based Filtering
# -------------------------------

# Fill missing product descriptions and compute TF-IDF matrix
products_df["description"] = products_df["description"].fillna("")
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(products_df["description"])

def recommend_content(query, top_n=10):
    """
    Recommend products based on the content (text) similarity with the query.
    """
    query_vec = tfidf.transform([query])
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    indices = np.argsort(cosine_sim)[::-1][:top_n]
    recommendations = products_df.iloc[indices][["product_id", "title", "description"]]
    return recommendations

# -------------------------------
# Collaborative Filtering using Graph-Based Approach
# -------------------------------

# Create a bipartite graph: users and products
G = nx.Graph()
for _, row in interactions_df.iterrows():
    user = f"user_{row['user_id']}"
    product = f"product_{row['product_id']}"
    # Weight can be based on purchase count; here we use the 'purchases' field.
    weight = row["purchases"]
    if weight > 0:  # only add meaningful interactions
        G.add_edge(user, product, weight=weight)

def recommend_collaborative(user_id, top_n=10):
    """
    Recommend products based on collaborative filtering using a graph-based approach.
    """
    user_node = f"user_{user_id}"
    if user_node not in G:
        return pd.DataFrame()  # No interaction data for this user

    # Collect products from neighbors (products connected to similar users)
    score_dict = {}
    for neighbor in G.neighbors(user_node):
        # For each product connected to the user
        if neighbor.startswith("product_"):
            score_dict[neighbor] = score_dict.get(neighbor, 0) + G[user_node][neighbor]["weight"]

    # Sort products based on aggregated weight
    sorted_scores = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    product_ids = [int(item[0].split("_")[1]) for item in sorted_scores][:top_n]
    recommendations = products_df[products_df["product_id"].isin(product_ids)]
    return recommendations[["product_id", "title", "description"]]

# -------------------------------
# Hybrid Model: Combining Both Approaches
# -------------------------------

def hybrid_recommend(user_id, query="", alpha=0.5, top_n=10):
    """
    Generate hybrid recommendations combining:
      - Content-based filtering (if a query is provided)
      - Collaborative filtering (based on user behavior)
    The parameter 'alpha' controls the weighting between the two approaches.
    """
    # Get content-based recommendations if a query is provided
    if query:
        content_recs = recommend_content(query, top_n=top_n)
    else:
        content_recs = pd.DataFrame()

    # Get collaborative recommendations
    collab_recs = recommend_collaborative(user_id, top_n=top_n)
    
    # For demonstration, simply concatenate and drop duplicates.
    # In practice, you would score and combine them based on confidence levels.
    combined = pd.concat([content_recs, collab_recs]).drop_duplicates(subset=["product_id"])
    combined = combined.head(top_n)
    return combined

# -------------------------------
# Example Usage
# -------------------------------
if __name__ == "__main__":
    # Example: Get recommendations for a given user and query
    sample_user_id = interactions_df["user_id"].iloc[0]  # Using the first user in the dataset
    sample_query = "wireless headphones"  # Sample search query
    recommendations = hybrid_recommend(sample_user_id, query=sample_query, alpha=0.5, top_n=5)
    print("Hybrid Recommendations:")
    print(recommendations)
