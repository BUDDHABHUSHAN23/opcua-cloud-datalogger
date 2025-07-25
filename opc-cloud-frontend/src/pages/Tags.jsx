// import { useEffect, useState } from 'react';
// import TagTreeBrowser from '../components/TagTreeBrowser';

// export default function Tags() {
//   const [groups, setGroups] = useState([]);
//   const [selectedGroup, setSelectedGroup] = useState('');
//   const [serverId, setServerId] = useState('');
//   const [selectedTags, setSelectedTags] = useState([]);
//   const [message, setMessage] = useState('');
//   const [error, setError] = useState('');

//   useEffect(() => {
//     fetch('/api/groups')
//       .then(res => res.json())
//       .then(setGroups)
//       .catch(() => setError('Failed to load groups.'));
//   }, []);

//   const handleTagSelect = (tagNode) => {
//     setSelectedTags(prev =>
//       prev.some(t => t.node_id === tagNode.node_id)
//         ? prev.filter(t => t.node_id !== tagNode.node_id)
//         : [...prev, tagNode]
//     );
//   };

//   const handleSubmit = async () => {
//     setMessage('');
//     setError('');

//     if (!selectedGroup || !serverId || selectedTags.length === 0) {
//       setError('Please select a server, group, and at least one tag.');
//       return;
//     }

//     const payload = {
//       group_id: parseInt(selectedGroup),
//       tags: selectedTags.map(t => ({
//         alias: t.display_name || t.node_id,
//         node_id: t.node_id,
//         data_type: 'float',
//         sampling_rate: 5,
//         enabled: true
//       }))
//     };

//     try {
//       const res = await fetch('/api/tags/batch', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(payload)
//       });

//       const result = await res.json();

//       if (res.ok) {
//         setSelectedTags([]);
//         setMessage('✅ Tags added successfully.');
//       } else {
//         setError(result.detail || '❌ Failed to add tags.');
//       }
//     } catch (err) {
//       setError('❌ Could not connect to the backend.');
//     }
//   };

//   return (
//     <div className="p-6">
//       <h1 className="text-2xl font-bold mb-4">Tag Manager</h1>

//       <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
//         <div className="space-y-4">
//           <div>
//             <label className="block font-medium">Select Group</label>
//             <select
//               value={selectedGroup}
//               onChange={(e) => setSelectedGroup(e.target.value)}
//               className="w-full border rounded px-3 py-2"
//             >
//               <option value="">-- Select Group --</option>
//               {groups.map(g => (
//                 <option key={g.id} value={g.id}>{g.name}</option>
//               ))}
//             </select>
//           </div>

//           <div>
//             <label className="block font-medium">Server ID</label>
//             <input
//               type="number"
//               value={serverId}
//               onChange={(e) => setServerId(e.target.value)}
//               className="w-full border rounded px-3 py-2"
//               placeholder="e.g. 1"
//             />
//           </div>

//           <div>
//             <button
//               onClick={handleSubmit}
//               className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
//             >
//               ➕ Add Selected Tags
//             </button>
//           </div>

//           {message && <div className="text-green-600 text-sm">{message}</div>}
//           {error && <div className="text-red-600 text-sm">{error}</div>}
//         </div>

//         <div>
//           <TagTreeBrowser serverId={serverId} onTagSelect={handleTagSelect} />
//         </div>
//       </div>
//     </div>
//   );
// }

import { useEffect, useState } from 'react';
import TagTreeBrowser from '../components/TagTreeBrowser';

export default function Tags() {
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState('');
  const [serverId, setServerId] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/api/groups').then(res => res.json()).then(setGroups);
  }, []);

  const handleTagSelect = (tagNode) => {
    setSelectedTags(prev =>
      prev.some(t => t.node_id === tagNode.node_id)
        ? prev.filter(t => t.node_id !== tagNode.node_id)
        : [...prev, tagNode]
    );
  };

  const handleSubmit = async () => {
    if (!selectedGroup || selectedTags.length === 0) {
      setMessage('Please select group and at least one tag.');
      return;
    }

    const payload = {
      group_id: parseInt(selectedGroup),
      tags: selectedTags.map(t => ({
        alias: t.display_name,
        node_id: t.node_id,
        data_type: 'float',
        sampling_rate: 5,
        enabled: true
      }))
    };

    const res = await fetch('/api/tags/batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(r => r.json());

    if (res.success) {
      setSelectedTags([]);
      setMessage('Tags added successfully!');
    } else {
      setMessage(res.detail || 'Failed to add tags');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Tag Manager</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Select Group</label>
            <select
              value={selectedGroup}
              onChange={(e) => setSelectedGroup(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
            >
              <option value="">-- Select Group --</option>
              {groups.map(g => (
                <option key={g.id} value={g.id}>{g.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium">Server ID</label>
            <input
              value={serverId}
              onChange={(e) => setServerId(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
              placeholder="1"
            />
          </div>

          <button
            onClick={handleSubmit}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Add Selected Tags
          </button>

          {message && <div className="text-sm text-blue-600">{message}</div>}
        </div>

        <TagTreeBrowser serverId={serverId} onTagSelect={handleTagSelect} />
      </div>
    </div>
  );
}
