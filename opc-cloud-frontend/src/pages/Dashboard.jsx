// import { useEffect, useState, useRef, useContext } from 'react';
// import { AuthContext } from '../context/AuthContext';

// export default function Dashboard() {
//   const [servers, setServers] = useState([]);
//   const [groups, setGroups] = useState([]);
//   const [tags, setTags] = useState([]);
//   const [selectedServer, setSelectedServer] = useState(null);
//   const [selectedGroup, setSelectedGroup] = useState(null);
//   const [selectedTags, setSelectedTags] = useState([]);
//   const [values, setValues] = useState([]);
//   const [error, setError] = useState('');
//   const socketRef = useRef(null);
//   const { token } = useContext(AuthContext);

//   useEffect(() => {
//     fetch('/api/servers/')
//       .then(res => res.json())
//       .then(setServers)
//       .catch(() => setError('Failed to load servers'));
//   }, []);

//   useEffect(() => {
//     if (!selectedServer) return;
//     fetch(`/api/groups?server_id=${selectedServer.id}`)
//       .then(res => res.json())
//       .then(setGroups)
//       .catch(() => setError('Failed to load groups'));
//   }, [selectedServer]);

//   useEffect(() => {
//     if (!selectedGroup) return;
//     fetch(`/api/tags/${selectedGroup.id}`)
//       .then(res => res.json())
//       .then(setTags)
//       .catch(() => setError('Failed to load tags'));
//   }, [selectedGroup]);

//   useEffect(() => {
//     if (!selectedTags.length || !selectedServer) return;

//     const ws = new WebSocket(`ws://localhost:8000/api/ws/monitor?token=${token}`);
//     socketRef.current = ws;

//     ws.onopen = () => {
//       ws.send(JSON.stringify({
//         server_url: selectedServer.endpoint_url,
//         node_ids: selectedTags.map(tag => tag.node_id)
//       }));
//     };

//     ws.onmessage = (e) => {
//       const data = JSON.parse(e.data);
//       if (data.values) setValues(data.values);
//       else if (Array.isArray(data)) setValues(data);
//     };

//     ws.onerror = () => setError('WebSocket error');
//     ws.onclose = () => console.log('WebSocket closed');

//     return () => ws.close();
//   }, [selectedTags]);

//   return (
//     <div className="p-6 space-y-4">
//       <h1 className="text-2xl font-bold">Live Monitor</h1>

//       {error && <div className="text-red-500">{error}</div>}

//       <select onChange={e => {
//         const srv = servers.find(s => s.id === parseInt(e.target.value));
//         setSelectedServer(srv);
//         setGroups([]); setTags([]); setSelectedTags([]); setValues([]);
//       }} className="border p-2">
//         <option value="">Select Server</option>
//         {servers.map(s => (
//           <option key={s.id} value={s.id}>{s.name}</option>
//         ))}
//       </select>

//       {groups.length > 0 && (
//         <select onChange={e => {
//           const grp = groups.find(g => g.id === parseInt(e.target.value));
//           setSelectedGroup(grp);
//           setTags([]); setSelectedTags([]); setValues([]);
//         }} className="border p-2">
//           <option value="">Select Group</option>
//           {groups.map(g => (
//             <option key={g.id} value={g.id}>{g.name}</option>
//           ))}
//         </select>
//       )}

//       {tags.length > 0 && (
//         <div className="space-y-2">
//           <label className="font-semibold">Select Tags:</label>
//           <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
//             {tags.map(tag => (
//               <label key={tag.id} className="block">
//                 <input
//                   type="checkbox"
//                   checked={selectedTags.some(t => t.id === tag.id)}
//                   onChange={() => {
//                     setSelectedTags(prev =>
//                       prev.some(t => t.id === tag.id)
//                         ? prev.filter(t => t.id !== tag.id)
//                         : [...prev, tag]
//                     );
//                   }}
//                 /> {tag.alias || tag.node_id}
//               </label>
//             ))}
//           </div>
//         </div>
//       )}

//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
//         {values.map((tag, i) => (
//           <div key={i} className="p-4 rounded shadow border-l-4 bg-white"
//                style={{ borderColor: tag.quality === 'Good' ? 'green' : tag.quality === 'Bad' ? 'red' : 'orange' }}>
//             <div className="font-semibold">{tag.alias || tag.nodeId}</div>
//             {tag.error ? (
//               <div className="text-red-600">Error: {tag.error}</div>
//             ) : (
//               <>
//                 <div className="text-sm">Value: {tag.value}</div>
//                 <div className="text-sm">Time: {tag.timestamp}</div>
//                 <div className="text-sm">Quality: {tag.quality}</div>
//               </>
//             )}
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }
import { useEffect, useState, useRef, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function Dashboard() {
  const [servers, setServers] = useState([]);
  const [groups, setGroups] = useState([]);
  const [tags, setTags] = useState([]);
  const [selectedServer, setSelectedServer] = useState(null);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [selectedTags, setSelectedTags] = useState([]);
  const [values, setValues] = useState([]);
  const [error, setError] = useState('');
  const socketRef = useRef(null);
  const { token } = useContext(AuthContext);

  useEffect(() => {
    fetch('/api/servers/')
      .then(res => res.json())
      .then(setServers)
      .catch(() => setError('Failed to load servers'));
  }, []);

  useEffect(() => {
    if (!selectedServer) return;
    fetch(`/api/groups?server_id=${selectedServer.id}`)
      .then(res => res.json())
      .then(setGroups)
      .catch(() => setError('Failed to load groups'));
  }, [selectedServer]);

  useEffect(() => {
    if (!selectedGroup) return;
    fetch(`/api/tags/${selectedGroup.id}`)
      .then(res => res.json())
      .then(setTags)
      .catch(() => setError('Failed to load tags'));
  }, [selectedGroup]);

  useEffect(() => {
    if (!selectedTags.length || !selectedServer) return;

    const ws = new WebSocket(`ws://localhost:8000/api/ws/monitor?token=${token}`);
    socketRef.current = ws;

    ws.onopen = () => {
      ws.send(JSON.stringify({
        server_url: selectedServer.endpoint_url,
        node_ids: selectedTags.map(tag => tag.node_id)
      }));
    };

    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.values) setValues(data.values);
      else if (Array.isArray(data)) setValues(data);
    };

    ws.onerror = () => setError('WebSocket error');
    ws.onclose = () => console.log('WebSocket closed');

    return () => ws.close();
  }, [selectedTags]);

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Live Monitor</h1>

      {error && <div className="text-red-500">{error}</div>}

      <select onChange={e => {
        const srv = servers.find(s => s.id === parseInt(e.target.value));
        setSelectedServer(srv);
        setGroups([]); setTags([]); setSelectedTags([]); setValues([]);
      }} className="border p-2">
        <option value="">Select Server</option>
        {servers.map(s => (
          <option key={s.id} value={s.id}>{s.name}</option>
        ))}
      </select>

      {groups.length > 0 && (
        <select onChange={e => {
          const grp = groups.find(g => g.id === parseInt(e.target.value));
          setSelectedGroup(grp);
          setTags([]); setSelectedTags([]); setValues([]);
        }} className="border p-2">
          <option value="">Select Group</option>
          {groups.map(g => (
            <option key={g.id} value={g.id}>{g.name}</option>
          ))}
        </select>
      )}

      {tags.length > 0 && (
        <div className="space-y-2">
          <label className="font-semibold">Select Tags:</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {tags.map(tag => (
              <label key={tag.id} className="block">
                <input
                  type="checkbox"
                  checked={selectedTags.some(t => t.id === tag.id)}
                  onChange={() => {
                    setSelectedTags(prev =>
                      prev.some(t => t.id === tag.id)
                        ? prev.filter(t => t.id !== tag.id)
                        : [...prev, tag]
                    );
                  }}
                /> {tag.alias || tag.node_id}
              </label>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {values.map((tag, i) => (
          <div key={i} className="p-4 rounded shadow border-l-4 bg-white"
               style={{ borderColor: tag.quality === 'Good' ? 'green' : tag.quality === 'Bad' ? 'red' : 'orange' }}>
            <div className="font-semibold">{tag.alias || tag.nodeId}</div>
            {tag.error ? (
              <div className="text-red-600">Error: {tag.error}</div>
            ) : (
              <>
                <div className="text-sm">Value: {tag.value}</div>
                <div className="text-sm">Time: {tag.timestamp}</div>
                <div className="text-sm">Quality: {tag.quality}</div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
