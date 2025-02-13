import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Database connection setup
DB_URL = "postgresql://username:password@localhost:5432/recommendation_db"
engine = create_engine(DB_URL)

# Load datasets
users_df = pd.read_csv("../data/large_users.csv")
products_df = pd.read_csv("../data/large_products.csv")
interactions_df = pd.read_csv("../data/large_interactions.csv")

# Preprocessing: Handle missing values
users_df.fillna("Unknown", inplace=True)
products_df.fillna("Unknown", inplace=True)
interactions_df.fillna(0, inplace=True)

# Store data into PostgreSQL
def save_to_db(df, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)

save_to_db(users_df, "users")
save_to_db(products_df, "products")
save_to_db(interactions_df, "interactions")

print("Data successfully loaded into PostgreSQL!")