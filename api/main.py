from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from hybrid_model import hybrid_recommend  # Ensure this file is in your PYTHONPATH

app = FastAPI(title="Hybrid Multi-Modal AI Recommendation Engine API")

class RecommendationRequest(BaseModel):
    user_id: str
    query: Optional[str] = ""
    alpha: Optional[float] = 0.5
    top_n: Optional[int] = 10

@app.post("/recommendations")
def get_recommendations(request: RecommendationRequest):
    try:
        recommendations = hybrid_recommend(
            user_id=request.user_id, 
            query=request.query, 
            alpha=request.alpha, 
            top_n=request.top_n
        )
        # Convert DataFrame to a list of dictionaries
        return recommendations.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
