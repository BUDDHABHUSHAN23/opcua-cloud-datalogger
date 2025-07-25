// import { useEffect, useState, useRef, useContext } from 'react';
// import { AuthContext } from "../context/AuthContext";

// export default function TagMonitor() {
//   const [servers, setServers] = useState([]);
//   const [groups, setGroups] = useState([]);
//   const [tags, setTags] = useState([]);
//   const [selectedServer, setSelectedServer] = useState('');
//   const [selectedGroup, setSelectedGroup] = useState('');
//   const [selectedTags, setSelectedTags] = useState([]);
//   const [messages, setMessages] = useState([]);
//   const socketRef = useRef(null);
//   const { token } = useContext(AuthContext);

//   // Fetch servers on mount
//   useEffect(() => {
//     fetch('/api/servers')
//       .then(res => res.json())
//       .then(data => setServers(data));
//   }, []);

//   // Fetch groups when server is selected
//   useEffect(() => {
//     if (selectedServer) {
//       fetch(`/api/groups?server_id=${selectedServer}`)
//         .then(res => res.json())
//         .then(data => setGroups(data));
//     }
//   }, [selectedServer]);

//   // Fetch tags when group is selected
//   useEffect(() => {
//     if (selectedGroup) {
//       fetch(`/api/tags/group/${selectedGroup}`)
//         .then(res => res.json())
//         .then(data => setTags(data));
//     }
//   }, [selectedGroup]);

//   // Open WebSocket once tags are selected
//   useEffect(() => {
//     if (!token || selectedTags.length === 0 || !selectedServer) return;

//     const serverObj = servers.find(s => s.id === parseInt(selectedServer));
//     const serverUrl = serverObj?.endpoint_url || '';

//     const nodeIds = tags
//       .filter(tag => selectedTags.includes(tag.id))
//       .map(tag => tag.node_id);

//     const ws = new WebSocket(`ws://localhost:8000/api/ws/monitor?token=${token}`);
//     socketRef.current = ws;

//     ws.onopen = () => {
//       ws.send(JSON.stringify({ server_url: serverUrl, node_ids: nodeIds }));
//     };

//     ws.onmessage = (event) => {
//       const data = JSON.parse(event.data);
//       if (data.values) {
//         setMessages((prev) => [...prev.slice(-49), ...data.values]);
//       } else if (data.error) {
//         console.error("WebSocket Error:", data.error);
//       }
//     };

//     ws.onerror = (err) => console.error("WebSocket error:", err);
//     ws.onclose = () => console.log("WebSocket closed");

//     return () => {
//       if (socketRef.current) socketRef.current.close();
//     };
//   }, [selectedTags, selectedServer, token]);

//   return (
//     <div className="p-6">
//       <h2 className="text-xl font-bold mb-4">Live Tag Monitor</h2>

//       <div className="flex gap-4 mb-4">
//         <select className="p-2 border rounded" value={selectedServer} onChange={e => setSelectedServer(e.target.value)}>
//           <option value="">Select Server</option>
//           {servers.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
//         </select>

//         <select className="p-2 border rounded" value={selectedGroup} onChange={e => setSelectedGroup(e.target.value)} disabled={!selectedServer}>
//           <option value="">Select Group</option>
//           {groups.map(g => <option key={g.id} value={g.id}>{g.name}</option>)}
//         </select>

//         <select
//           multiple
//           className="p-2 border rounded w-60 h-32"
//           value={selectedTags}
//           onChange={e => setSelectedTags(Array.from(e.target.selectedOptions, o => parseInt(o.value)))}
//           disabled={!selectedGroup}
//         >
//           {tags.map(tag => <option key={tag.id} value={tag.id}>{tag.alias || tag.node_id}</option>)}
//         </select>
//       </div>

//       <div className="bg-white p-4 rounded shadow max-h-[400px] overflow-y-auto text-sm font-mono">
//         {messages.map((msg, idx) => (
//           <div key={idx} className="mb-1">
//             {msg.timestamp} → <strong>{msg.alias || msg.nodeId}:</strong> {msg.value} ({msg.quality})
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }
import { useEffect, useState, useRef, useContext } from 'react';
import { AuthContext } from "../context/AuthContext";

export default function TagMonitor() {
  const [servers, setServers] = useState([]);
  const [groups, setGroups] = useState([]);
  const [tags, setTags] = useState([]);
  const [selectedServer, setSelectedServer] = useState('');
  const [selectedGroup, setSelectedGroup] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [messages, setMessages] = useState([]);
  const socketRef = useRef(null);
  const { token } = useContext(AuthContext);

  // Fetch servers on mount
  useEffect(() => {
    fetch('/api/servers/')
      .then(res => res.json())
      .then(data => setServers(data));
  }, []);

  // Fetch groups when server is selected
  useEffect(() => {
    if (selectedServer) {
      fetch(`/api/groups?server_id=${selectedServer}`)
        .then(res => res.json())
        .then(data => setGroups(data));
    }
  }, [selectedServer]);

  // Fetch tags when group is selected
  useEffect(() => {
    if (selectedGroup) {
      fetch(`/api/tags/group/${selectedGroup}`)
        .then(res => res.json())
        .then(data => setTags(data));
    }
  }, [selectedGroup]);

  // Open WebSocket once tags are selected
  useEffect(() => {
    if (!token || selectedTags.length === 0 || !selectedServer) return;

    const serverObj = servers.find(s => s.id === parseInt(selectedServer));
    const serverUrl = serverObj?.endpoint_url || '';

    const nodeIds = tags
      .filter(tag => selectedTags.includes(tag.id))
      .map(tag => tag.node_id);

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
  }, [selectedTags, selectedServer, token]);

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold mb-4">Live Tag Monitor</h2>

      <div className="flex gap-4 mb-4">
        <select className="p-2 border rounded" value={selectedServer} onChange={e => setSelectedServer(e.target.value)}>
          <option value="">Select Server</option>
          {servers.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>

        <select className="p-2 border rounded" value={selectedGroup} onChange={e => setSelectedGroup(e.target.value)} disabled={!selectedServer}>
          <option value="">Select Group</option>
          {groups.map(g => <option key={g.id} value={g.id}>{g.name}</option>)}
        </select>

        <select
          multiple
          className="p-2 border rounded w-60 h-32"
          value={selectedTags}
          onChange={e => setSelectedTags(Array.from(e.target.selectedOptions, o => parseInt(o.value)))}
          disabled={!selectedGroup}
        >
          {tags.map(tag => <option key={tag.id} value={tag.id}>{tag.alias || tag.node_id}</option>)}
        </select>
      </div>

      <div className="bg-white p-4 rounded shadow max-h-[400px] overflow-y-auto text-sm font-mono">
        {messages.map((msg, idx) => (
          <div key={idx} className="mb-1">
            {msg.timestamp} → <strong>{msg.alias || msg.nodeId}:</strong> {msg.value} ({msg.quality})
          </div>
        ))}
      </div>
    </div>
  );
}
