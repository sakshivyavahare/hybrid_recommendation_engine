import pandas as pd
import networkx as nx

# Load datasets (adjust paths as necessary)
interactions_df = pd.read_csv("../data/large_interactions.csv")
products_df = pd.read_csv("../data/large_products.csv")

# Build a bipartite graph: Users and Products
G = nx.Graph()

for _, row in interactions_df.iterrows():
    user_node = f"user_{row['user_id']}"
    product_node = f"product_{row['product_id']}"
    weight = row["purchases"]  # Using purchase count as weight
    if weight > 0:  # Only add meaningful interactions
        G.add_edge(user_node, product_node, weight=weight)

def gnn_recommend(user_id, top_n=10):
    """
    Recommend products based on collaborative filtering using a graph-based approach.
    """
    user_node = f"user_{user_id}"
    if user_node not in G:
        print("No interactions found for this user.")
        return pd.DataFrame()  # Return empty DataFrame if no data for user

    scores = {}
    # Direct neighbor contributions (user -> product)
    for neighbor in G.neighbors(user_node):
        if neighbor.startswith("product_"):
            scores[neighbor] = scores.get(neighbor, 0) + G[user_node][neighbor]["weight"]
    
    # Second-order neighbors (user -> other user -> product)
    for neighbor in G.neighbors(user_node):
        if neighbor.startswith("user_"):
            for prod in G.neighbors(neighbor):
                if prod.startswith("product_"):
                    # Apply a decay factor (e.g., 0.5) for second-order hops
                    scores[prod] = scores.get(prod, 0) + G[neighbor][prod]["weight"] * 0.5

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    product_ids = [p.split("_")[1] for p, _ in sorted_scores]
    recommendations = products_df[products_df["product_id"].isin(product_ids)]
    return recommendations[["product_id", "title", "description"]]

# Example usage:
if __name__ == "__main__":
    sample_user_id = interactions_df["user_id"].iloc[0]  # Example user
    recs = gnn_recommend(sample_user_id, top_n=5)
    print("GNN-Based Collaborative Filtering Recommendations:")
    print(recs)
