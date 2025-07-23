
import { useEffect, useState, useRef, useContext } from 'react';
import { AuthContext } from "../context/AuthContext";  // ✅ Correct relative path


export default function TagMonitor() {
  const [messages, setMessages] = useState([]);
  const socketRef = useRef(null);
  const { token } = useContext(AuthContext);

  useEffect(() => {
    const serverUrl = "opc.tcp://localhost:4840"; // Or dynamically based on user
    const nodeIds = ["ns=2;s=Demo.Dynamic.Scalar.Float", "ns=2;s=Demo.Dynamic.Scalar.Int32"];
    if (!token) {
      console.error("No authentication token found");
      return;
    }
    const ws = new WebSocket(`ws://localhost:8000/api/ws/monitor?token=${token}`);
    socketRef.current = ws;

    ws.onopen = () => {
      ws.send(JSON.stringify({ server_url: serverUrl, node_ids: nodeIds }));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.values) {
        setMessages((prev) => [...prev.slice(-49), ...data.values]);
      } else if (data.error) {
        console.error("WebSocket Error:", data.error);
      }
    };

    ws.onerror = (err) => console.error("WebSocket error:", err);
    ws.onclose = () => console.log("WebSocket closed");

    return () => {
      if (socketRef.current) socketRef.current.close();
    };
  }, [token]);

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">Live Tag Monitor</h2>
      <div className="bg-white p-4 rounded shadow max-h-[400px] overflow-y-auto text-sm font-mono">
        {messages.map((msg, idx) => (
          <div key={idx}>
            {msg.timestamp} → <strong>{msg.alias || msg.nodeId}:</strong> {msg.value} ({msg.quality})
          </div>
        ))}
      </div>
    </div>
  );
}
