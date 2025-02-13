import React, { useState } from 'react';

const RecommendationDashboard = () => {
  const [userId, setUserId] = useState('');
  const [query, setQuery] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async () => {
    try {
      const response = await fetch('http://localhost:8000/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          query: query,
          alpha: 0.5,
          top_n: 10,
        }),
      });
      const data = await response.json();
      setRecommendations(data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Product Recommendations</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="border p-2 mr-2"
        />
        <input
          type="text"
          placeholder="Enter your search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-2 mr-2"
        />
        <button onClick={fetchRecommendations} className="bg-blue-500 text-white p-2">
          Get Recommendations
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recommendations.map((product, index) => (
          <div key={index} className="border p-4 rounded shadow">
            <h2 className="font-semibold">{product.title}</h2>
            <p>{product.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationDashboard;
