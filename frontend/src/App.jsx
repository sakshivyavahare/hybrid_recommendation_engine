import React from 'react';
import RecommendationDashboard from './components/RecommendationDashboard';
import Chatbot from 'C:\Users\vyava\OneDrive\Desktop\hybrid_recommendation_engine\frontend\src\components\Chatbot.jsx';
import RealTimeUpdates from './components/RealTimeUpdates';

const App = () => {
  return (
    <div className="container mx-auto p-4">
      <RecommendationDashboard />
      <Chatbot />
      <RealTimeUpdates />
    </div>
  );
};

export default App;
