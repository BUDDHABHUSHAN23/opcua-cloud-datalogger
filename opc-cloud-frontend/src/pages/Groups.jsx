
// import { useEffect, useState } from 'react';
// import { fetchGroups, fetchServers } from '../services/api';

// export default function Groups() {
//   const [groups, setGroups] = useState([]);
//   const [servers, setServers] = useState([]);
//   const [name, setName] = useState('');
//   const [serverId, setServerId] = useState('');
//   const [mode, setMode] = useState('Interval');
//   const [value, setValue] = useState('');
//   const [error, setError] = useState('');

//   useEffect(() => {
//     fetchServers().then(setServers);
//     fetchGroups().then(setGroups);
//   }, []);

//   const handleAdd = async () => {
//     if (!name || !serverId || !value) {
//       setError('All fields are required.');
//       return;
//     }

//     const payload = {
//       name,
//       server_id: parseInt(serverId),
//       mode,
//       value
//     };

//     const res = await fetch('/api/groups', {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(payload)
//     }).then(res => res.json());

//     if (res.success || res.id) {
//       setName('');
//       setServerId('');
//       setValue('');
//       setMode('Interval');
//       setError('');
//       fetchGroups().then(setGroups);
//     } else {
//       setError(res.detail || 'Failed to add group');
//     }
//   };

//   const handleDelete = async (id) => {
//     await fetch(`/api/groups/${id}`, { method: 'DELETE' });
//     fetchGroups().then(setGroups);
//   };

//   return (
//     <div className="p-6">
//       <h1 className="text-2xl font-bold mb-4">Groups</h1>

//       <div className="bg-white p-4 rounded shadow-md mb-6 max-w-xl">
//         <div className="mb-2">
//           <label className="block text-sm font-medium">Group Name</label>
//           <input
//             value={name}
//             onChange={(e) => setName(e.target.value)}
//             className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
//             placeholder="Group A"
//           />
//         </div>
//         <div className="mb-2">
//           <label className="block text-sm font-medium">Select Server</label>
//           <select
//             value={serverId}
//             onChange={(e) => setServerId(e.target.value)}
//             className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
//           >
//             <option value="">-- Select --</option>
//             {servers.map(s => (
//               <option key={s.id} value={s.id}>{s.name}</option>
//             ))}
//           </select>
//         </div>
//         <div className="mb-2">
//           <label className="block text-sm font-medium">Mode</label>
//           <select
//             value={mode}
//             onChange={(e) => setMode(e.target.value)}
//             className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
//           >
//             <option value="Interval">Interval</option>
//             <option value="Clock">Clock</option>
//             <option value="SpecificTime">Specific Time</option>
//           </select>
//         </div>
//         <div className="mb-2">
//           <label className="block text-sm font-medium">
//             {mode === 'Interval' ? 'Interval (sec)' : mode === 'Clock' ? 'Time (HH:MM)' : 'Specific DateTime'}
//           </label>
//           <input
//             value={value}
//             onChange={(e) => setValue(e.target.value)}
//             className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
//             placeholder={mode === 'Interval' ? 'e.g., 10' : 'e.g., 14:00 or 2025-07-20T15:30'}
//           />
//         </div>
//         {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
//         <button
//           onClick={handleAdd}
//           className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
//         >
//           Add Group
//         </button>
//       </div>

//       <div className="max-w-xl">
//         <h2 className="text-xl font-semibold mb-2">Defined Groups</h2>
//         {groups.length === 0 ? (
//           <div className="text-gray-500">No groups defined.</div>
//         ) : (
//           <ul className="space-y-2">
//             {groups.map((grp) => (
//               <li key={grp.id} className="flex justify-between items-center bg-gray-100 p-3 rounded">
//                 <div>
//                   <div className="font-medium">{grp.name}</div>
//                   <div className="text-sm text-gray-600">Mode: {grp.mode} — Value: {grp.value}</div>
//                 </div>
//                 <button
//                   onClick={() => handleDelete(grp.id)}
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
import { fetchGroups, fetchServers } from '../services/api';

export default function Groups() {
  const [groups, setGroups] = useState([]);
  const [servers, setServers] = useState([]);
  const [name, setName] = useState('');
  const [serverId, setServerId] = useState('');
  const [mode, setMode] = useState('Interval');
  const [value, setValue] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchServers().then(setServers);
    fetchGroups().then(setGroups);
  }, []);

  const handleAdd = async () => {
    if (!name || !serverId || !value) {
      setError('All fields are required.');
      return;
    }

    const payload = {
      name,
      server_id: parseInt(serverId),
      mode,
      value
    };

    const res = await fetch('/api/groups', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(res => res.json());

    if (res.success || res.id) {
      setName('');
      setServerId('');
      setValue('');
      setMode('Interval');
      setError('');
      fetchGroups().then(setGroups);
    } else {
      setError(res.detail || 'Failed to add group');
    }
  };

  const handleDelete = async (id) => {
    await fetch(`/api/groups/${id}`, { method: 'DELETE' });
    fetchGroups().then(setGroups);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Groups</h1>

      <div className="bg-white p-4 rounded shadow-md mb-6 max-w-xl">
        <div className="mb-2">
          <label className="block text-sm font-medium">Group Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
            placeholder="Group A"
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Select Server</label>
          <select
            value={serverId}
            onChange={(e) => setServerId(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          >
            <option value="">-- Select --</option>
            {servers.map(s => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Mode</label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          >
            <option value="Interval">Interval</option>
            <option value="Clock">Clock</option>
            <option value="SpecificTime">Specific Time</option>
          </select>
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">
            {mode === 'Interval' ? 'Interval (sec)' : mode === 'Clock' ? 'Time (HH:MM)' : 'Specific DateTime'}
          </label>
          <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
            placeholder={mode === 'Interval' ? 'e.g., 10' : 'e.g., 14:00 or 2025-07-20T15:30'}
          />
        </div>
        {error && <div className="text-red-600 text-sm mb-2">{error}</div>}
        <button
          onClick={handleAdd}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Add Group
        </button>
      </div>

      <div className="max-w-xl">
        <h2 className="text-xl font-semibold mb-2">Defined Groups</h2>
        {groups.length === 0 ? (
          <div className="text-gray-500">No groups defined.</div>
        ) : (
          <ul className="space-y-2">
            {groups.map((grp) => (
              <li key={grp.id} className="flex justify-between items-center bg-gray-100 p-3 rounded">
                <div>
                  <div className="font-medium">{grp.name}</div>
                  <div className="text-sm text-gray-600">Mode: {grp.mode} — Value: {grp.value}</div>
                </div>
                <button
                  onClick={() => handleDelete(grp.id)}
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
