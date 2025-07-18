
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [liveData, setLiveData] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/monitor');

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLiveData(data);
      } catch (e) {
        console.error("Invalid JSON:", e);
      }
    };

    socket.onerror = (e) => {
      console.error("WebSocket error:", e);
    };

    return () => {
      socket.close();
    };
  }, []);

  const getStatusColor = (status) => {
    if (!status) return 'bg-gray-300';
    if (status.toLowerCase().includes('good')) return 'bg-green-500 text-white';
    if (status.toLowerCase().includes('bad')) return 'bg-red-500 text-white';
    if (status.toLowerCase().includes('uncertain')) return 'bg-yellow-300 text-black';
    return 'bg-gray-300';
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Live Tag Monitor</h1>

      {liveData.length === 0 ? (
        <div className="text-gray-500">Waiting for live data...</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-left border border-collapse">
            <thead className="bg-gray-200">
              <tr>
                <th className="p-2 border">Group</th>
                <th className="p-2 border">Alias</th>
                <th className="p-2 border">Node ID</th>
                <th className="p-2 border">Value</th>
                <th className="p-2 border">Status</th>
              </tr>
            </thead>
            <tbody>
              {liveData.map((tag, idx) => (
                <tr key={idx} className="border-t">
                  <td className="p-2 border">{tag.group_name}</td>
                  <td className="p-2 border">{tag.alias}</td>
                  <td className="p-2 border text-xs">{tag.node_id}</td>
                  <td className="p-2 border">{tag.value}</td>
                  <td className={`p-2 border text-sm text-center ${getStatusColor(tag.status)}`}>
                    {tag.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
// export default function Dashboard() {
//   return (
//     <div className="p-6">
//       <h1 className="text-3xl font-bold text-blue-600">✅ Hello from Dashboard — Frontend is Working!</h1>
//     </div>
//   );
// }
