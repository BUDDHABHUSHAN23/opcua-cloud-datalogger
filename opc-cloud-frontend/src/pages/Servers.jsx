
// import { useEffect, useState } from 'react';
// import { fetchServers, addServer, deleteServer } from '../services/api';

// export default function Servers() {
//   const [servers, setServers] = useState([]);
//   const [name, setName] = useState('');
//   const [endpoint, setEndpoint] = useState('');
//   const [error, setError] = useState('');

//   useEffect(() => {
//     loadServers();
//   }, []);

//   const loadServers = async () => {
//     try {
//       const data = await fetchServers();
//       if (Array.isArray(data)) {
//         setServers(data);
//         setError('');
//       } else {
//         console.warn("Expected array, got:", data);
//         setError("Unexpected server response.");
//         setServers([]); // prevent map() crash
//       }
//     } catch (err) {
//       console.error("Failed to fetch servers:", err);
//       setError("Failed to fetch servers");
//     }
//   };


//   const handleAdd = async () => {
//     if (!name || !endpoint) {
//       setError('Both fields are required.');
//       return;
//     }
//     const res = await addServer(name, endpoint);
//     if (res.success) {
//       setName('');
//       setEndpoint('');
//       loadServers();
//       setError('');
//     } else {
//       setError(res.detail || 'Add failed');
//     }
//   };

//   const handleDelete = async (id) => {
//     await deleteServer(id);
//     loadServers();
//   };

//   return (
//     <div className="p-6">
//       <h1 className="text-2xl font-bold mb-4">OPC UA Servers</h1>

//       <div className="bg-white p-4 rounded shadow-md mb-6 max-w-xl">
//         <div className="mb-2">
//           <label className="block text-sm font-medium">Server Name</label>
//           <input
//             value={name}
//             onChange={(e) => setName(e.target.value)}
//             className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
//             placeholder="My OPC Server"
//           />
//         </div>
//         <div className="mb-2">
//           <label className="block text-sm font-medium">Endpoint URL</label>
//           <input
//             value={endpoint}
//             onChange={(e) => setEndpoint(e.target.value)}
//             className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
//             placeholder="opc.tcp://localhost:4840"
//           />
//         </div>
//         {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
//         <button
//           onClick={handleAdd}
//           className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
//         >
//           Add Server
//         </button>
//       </div>

//       <div className="max-w-xl">
//         <h2 className="text-xl font-semibold mb-2">Registered Servers</h2>
//         {servers.length === 0 ? (
//           <div className="text-gray-500">No servers found.</div>
//         ) : (
//           <ul className="space-y-2">
//             {servers.map((srv) => (
//               <li key={srv.id} className="flex justify-between items-center bg-gray-100 p-3 rounded">
//                 <div>
//                   <div className="font-medium">{srv.name}</div>
//                   <div className="text-sm text-gray-600">{srv.endpoint_url}</div>
//                 </div>
//                 <button
//                   onClick={() => handleDelete(srv.id)}
//                   className="text-red-600 hover:underline text-sm"
//                 >
//                   Delete
//                 </button>
//               </li>
//             ))}
//           </ul>
//         )}
//       </div>
//     </div>
//   );
// }

import { useEffect, useState } from 'react';
import { fetchServers, addServer, deleteServer } from '../services/api';

export default function Servers() {
  const [servers, setServers] = useState([]);
  const [name, setName] = useState('');
  const [endpoint, setEndpoint] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    loadServers();
  }, []);

  const loadServers = async () => {
    try {
      const data = await fetchServers();
      if (Array.isArray(data)) {
        setServers(data);
        setError('');
      } else {
        console.warn("Expected array, got:", data);
        setError("Unexpected server response.");
        setServers([]); // prevent map() crash
      }
    } catch (err) {
      console.error("Failed to fetch servers:", err);
      setError("Failed to fetch servers");
    }
  };


  const handleAdd = async () => {
    if (!name || !endpoint) {
      setError('Both fields are required.');
      return;
    }
    const res = await addServer(name, endpoint);
    if (res.success) {
      setName('');
      setEndpoint('');
      loadServers();
      setError('');
    } else {
      setError(res.detail || 'Add failed');
    }
  };

  const handleDelete = async (id) => {
    await deleteServer(id);
    loadServers();
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">OPC UA Servers</h1>

      <div className="bg-white p-4 rounded shadow-md mb-6 max-w-xl">
        <div className="mb-2">
          <label className="block text-sm font-medium">Server Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
            placeholder="My OPC Server"
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Endpoint URL</label>
          <input
            value={endpoint}
            onChange={(e) => setEndpoint(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
            placeholder="opc.tcp://localhost:4840"
          />
        </div>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <button
          onClick={handleAdd}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Add Server
        </button>
      </div>

      <div className="max-w-xl">
        <h2 className="text-xl font-semibold mb-2">Registered Servers</h2>
        {servers.length === 0 ? (
          <div className="text-gray-500">No servers found.</div>
        ) : (
          <ul className="space-y-2">
            {servers.map((srv) => (
              <li key={srv.id} className="flex justify-between items-center bg-gray-100 p-3 rounded">
                <div>
                  <div className="font-medium">{srv.name}</div>
                  <div className="text-sm text-gray-600">{srv.endpoint_url}</div>
                </div>
                <button
                  onClick={() => handleDelete(srv.id)}
                  className="text-red-600 hover:underline text-sm"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
