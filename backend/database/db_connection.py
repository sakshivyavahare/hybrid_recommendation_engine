import psycopg2
from psycopg2.extras import RealDictCursor
import redis

# PostgreSQL connection details - replace with your actual credentials
PG_CONFIG = {
    "dbname": "recommendation_db",
    "user": "username",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def get_pg_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Returns:
        connection: A psycopg2 connection object.
    """
    try:
        conn = psycopg2.connect(**PG_CONFIG, cursor_factory=RealDictCursor)
        print("Connected to PostgreSQL successfully.")
        return conn
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)
        return None

def close_pg_connection(conn):
    """
    Closes the PostgreSQL connection.
    """
    if conn:
        conn.close()
        print("PostgreSQL connection closed.")

# Redis connection details
REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}

def get_redis_connection():
    """
    Establishes a connection to the Redis server.
    Returns:
        redis_client: A Redis client object.
    """
    try:
        r = redis.Redis(**REDIS_CONFIG)
        r.ping()  # Test the connection
        print("Connected to Redis successfully.")
        return r
    except Exception as e:
        print("Error connecting to Redis:", e)
        return None

# Example usage
if __name__ == "__main__":
    # Test PostgreSQL connection
    conn = get_pg_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        print("Current time from PostgreSQL:", cur.fetchone())
        cur.close()
        close_pg_connection(conn)

    # Test Redis connection
    redis_client = get_redis_connection()
    if redis_client:
        print("Redis ping response:", redis_client.ping())
