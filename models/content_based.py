import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load products dataset
products_df = pd.read_csv("../data/large_products.csv")
products_df["description"] = products_df["description"].fillna("")

# Build TF-IDF matrix for product descriptions
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(products_df["description"])

def content_based_recommend(query, top_n=10):
    """
    Recommend products based on text similarity between the query and product descriptions.
    """
    query_vec = tfidf.transform([query])
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    indices = np.argsort(cosine_sim)[::-1][:top_n]
    recommendations = products_df.iloc[indices][["product_id", "title", "description"]]
    return recommendations

# Example usage:
if __name__ == "__main__":
    sample_query = "wireless headphones"
    recs = content_based_recommend(sample_query, top_n=5)
    print("Content-Based Recommendations:")
    print(recs)
