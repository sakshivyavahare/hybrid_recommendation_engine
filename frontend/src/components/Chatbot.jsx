import React, { useState } from 'react';

const Chatbot = () => {
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([]);

  const sendMessage = async () => {
    if (!message) return;
    
    // Append the user's message to the chat log
    setChatLog((prev) => [...prev, { sender: 'User', text: message }]);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 'sample_user', // Replace with actual user ID if available
          message: message,
        }),
      });
      const data = await response.json();
      setChatLog((prev) => [...prev, { sender: 'Bot', text: data.response }]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
    setMessage('');
  };

  return (
    <div className="p-6 border mt-4">
      <h1 className="text-xl font-bold mb-2">Chatbot Assistant</h1>
      <div className="h-64 overflow-y-scroll border p-2 mb-2">
        {chatLog.map((entry, idx) => (
          <div key={idx} className={`mb-1 ${entry.sender === 'Bot' ? 'text-blue-500' : 'text-gray-800'}`}>
            <strong>{entry.sender}: </strong>{entry.text}
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          type="text"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="border p-2 flex-grow"
        />
        <button onClick={sendMessage} className="bg-green-500 text-white p-2 ml-2">Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
