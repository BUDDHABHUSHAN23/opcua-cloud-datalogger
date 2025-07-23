
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [values, setValues] = useState([]);
  const [error, setError] = useState('');
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  useEffect(() => {
    let socket;
    let retryTimer;

    const baseWsUrl = import.meta.env.DEV
      ? 'ws://localhost:8000/api/ws/monitor'
      : 'ws://backend:8000/api/ws/monitor';

    const connect = () => {
      socket = new WebSocket(baseWsUrl);

      socket.onopen = () => {
        console.log("✅ WebSocket connected. Sending payload...");
        socket.send(JSON.stringify({
          server_url: "opc.tcp://192.168.5.189:62640/IntegrationObjects/ServerSimulator",
          node_ids: [
            "ns=2;s=Demo.Static.Scalar.Int32",
            "ns=2;s=Demo.Static.Scalar.Boolean"
          ]
        }));
      };

      socket.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          if (parsed.values && Array.isArray(parsed.values)) {
            setValues(parsed.values);
            setError('');
          } else if (Array.isArray(parsed)) {
            setValues(parsed);
            setError('');
          } else {
            setError("Unexpected data format from server");
            setValues(parsed); // fallback to show raw
            console.warn("Raw payload:", parsed);
          }
        } catch (err) {
          setError('Failed to parse server data');
          console.error("Parsing error:", err);
        }
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
      if (socket) socket.close();
    };
  }, [reconnectAttempts]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Live Monitor</h1>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.isArray(values) ? values.map((tag, i) => (
          <div key={i} className="bg-white p-4 rounded shadow border-l-4"
               style={{ borderColor: tag.quality === 'Good' ? 'green' : tag.quality === 'Bad' ? 'red' : 'orange' }}>
            <div className="font-semibold">{tag.alias || tag.nodeId}</div>
            {tag.error ? (
              <div className="text-sm text-red-600">Error: {tag.error}</div>
            ) : (
              <>
                <div className="text-sm text-gray-600">Value: {tag.value}</div>
                <div className="text-sm text-gray-600">Time: {tag.timestamp}</div>
                <div className="text-sm text-gray-600">Quality: {tag.quality}</div>
              </>
            )}
          </div>
        )) : (
          <pre className="mt-4 p-4 bg-gray-100 rounded text-xs overflow-x-auto">
            {JSON.stringify(values, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
