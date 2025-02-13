'''from fastapi import FastAPI, HTTPException
from database.db_queries import get_user_by_id, get_product_by_id, log_interaction
from database.redis_cache import get_cached_recommendations, cache_recommendations
from recommendation_engine.hybrid_model import get_hybrid_recommendations  # Import recommendation logic

app = FastAPI()

@app.post("/recommendations")
async def get_recommendations(user_id: str):
    # Check cache first
    cached_recs = get_cached_recommendations(user_id)
    if cached_recs:
        return {"source": "cache", "recommendations": cached_recs}

    # Fetch user details from DB
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate recommendations using hybrid model
    recommendations = get_hybrid_recommendations(user_id)

    # Cache recommendations
    cache_recommendations(user_id, recommendations)

    return {"source": "database", "recommendations": recommendations}

# Log user interactions
@app.post("/log_interaction")
async def log_user_interaction(user_id: str, product_id: str, interaction_type: str):
    log_interaction(user_id, product_id, interaction_type)
    return {"message": "Interaction logged successfully"}'''

from fastapi import FastAPI, HTTPException
from database.db_queries import get_user_by_id, get_product_by_id, log_interaction
from database.redis_cache import get_cached_recommendations, cache_recommendations
from models.hybrid_model import get_hybrid_recommendations # Import recommendation logic

app = FastAPI()

@app.post("/recommendations")
async def get_recommendations(user_id: str):
    try:
        # Check cache first
        cached_recs = get_cached_recommendations(user_id)
        if cached_recs:
            return {"source": "cache", "recommendations": cached_recs}

        # Fetch user details from DB
        user = get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate recommendations using hybrid model
        recommendations = get_hybrid_recommendations(user_id)

        # Cache recommendations
        cache_recommendations(user_id, recommendations)

        return {"source": "database", "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Log user interactions
@app.post("/log_interaction")
async def log_user_interaction(user_id: str, product_id: str, interaction_type: str):
    try:
        log_interaction(user_id, product_id, interaction_type)
        return {"message": "Interaction logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
