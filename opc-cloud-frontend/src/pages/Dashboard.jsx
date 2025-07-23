
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [values, setValues] = useState([]);
  const [error, setError] = useState('');
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  useEffect(() => {
    let socket;
    let retryTimer;

    const connect = () => {
      socket = new WebSocket("ws://localhost:8000/ws/monitor");
      socket.onmessage = (event) => {
        setValues(JSON.parse(event.data));
        setError('');
      };
      socket.onerror = () => setError('WebSocket error');
      socket.onclose = () => {
        setError('Disconnected. Reconnecting...');
        retryTimer = setTimeout(() => {
          setReconnectAttempts(prev => prev + 1);
          connect();
        }, 3000);
      };
    };

    connect();
    return () => {
      clearTimeout(retryTimer);
      socket && socket.close();
    };
  }, [reconnectAttempts]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Live Monitor</h1>
      {error && <div className="text-red-600">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {values.map((tag, i) => (
          <div key={i} className="bg-white p-4 rounded shadow border-l-4"
               style={{ borderColor: tag.quality === 'Good' ? 'green' : tag.quality === 'Bad' ? 'red' : 'orange' }}>
            <div className="font-semibold">{tag.alias}</div>
            <div className="text-sm text-gray-600">Value: {tag.value}</div>
            <div className="text-sm text-gray-600">Time: {tag.timestamp}</div>
            <div className="text-sm text-gray-600">Quality: {tag.quality}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
