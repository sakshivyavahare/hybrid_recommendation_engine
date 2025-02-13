import pandas as pd

def preprocess_users(file_path):
    df = pd.read_csv(file_path)
    df.fillna("Unknown", inplace=True)
    # Convert 'last_active' to datetime if present
    if "last_active" in df.columns:
        df["last_active"] = pd.to_datetime(df["last_active"], errors="coerce")
    return df

def preprocess_products(file_path):
    df = pd.read_csv(file_path)
    df.fillna("Unknown", inplace=True)
    return df

def preprocess_interactions(file_path):
    df = pd.read_csv(file_path)
    df.fillna(0, inplace=True)
    # Convert 'last_purchase_date' to datetime if present
    if "last_purchase_date" in df.columns:
        df["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"], errors="coerce")
    return df

if __name__ == "__main__":
    users_df = preprocess_users("../data/large_users.csv")
    products_df = preprocess_products("../data/large_products.csv")
    interactions_df = preprocess_interactions("../data/large_interactions.csv")
    
    print("Preprocessed Users Shape:", users_df.shape)
    print("Preprocessed Products Shape:", products_df.shape)
    print("Preprocessed Interactions Shape:", interactions_df.shape)
