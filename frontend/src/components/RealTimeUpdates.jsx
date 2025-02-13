import React, { useState, useEffect } from 'react';

const RealTimeUpdates = () => {
  const [updates, setUpdates] = useState([]);

  useEffect(() => {
    // Connect to the WebSocket server
    const socket = new WebSocket('ws://localhost:8000/api/ws/realtime');
    socket.onopen = () => console.log('Connected to real-time updates!');
    socket.onmessage = (event) => {
      setUpdates((prev) => [...prev, event.data]);
    };
    socket.onclose = () => console.log('Disconnected from real-time updates');

    // Clean up on component unmount
    return () => socket.close();
  }, []);

  return (
    <div className="p-6 border mt-4">
      <h1 className="text-xl font-bold mb-2">Real-Time Updates</h1>
      <div className="h-48 overflow-y-scroll border p-2">
        {updates.map((msg, idx) => (
          <div key={idx} className="mb-1 text-purple-600">{msg}</div>
        ))}
      </div>
    </div>
  );
};

export default RealTimeUpdates;
