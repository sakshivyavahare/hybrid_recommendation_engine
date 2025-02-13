from database.db_connection import get_redis_connection

redis_client = get_redis_connection()

# Cache user data for quick retrieval
def cache_user_data(user_id, user_data):
    redis_client.setex(f"user:{user_id}", 3600, str(user_data))  # Cache for 1 hour

# Fetch user data from cache
def get_cached_user_data(user_id):
    user_data = redis_client.get(f"user:{user_id}")
    return eval(user_data) if user_data else None

# Cache recommendations
def cache_recommendations(user_id, recommendations):
    redis_client.setex(f"recommendations:{user_id}", 1800, str(recommendations))  # Cache for 30 min

# Retrieve cached recommendations
def get_cached_recommendations(user_id):
    recommendations = redis_client.get(f"recommendations:{user_id}")
    return eval(recommendations) if recommendations else None
