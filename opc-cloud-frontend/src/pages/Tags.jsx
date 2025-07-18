
import { useEffect, useState } from 'react';

export default function Tags() {
  const [groups, setGroups] = useState([]);
  const [tags, setTags] = useState([]);
  const [groupId, setGroupId] = useState('');
  const [alias, setAlias] = useState('');
  const [nodeId, setNodeId] = useState('');
  const [dataType, setDataType] = useState('float');
  const [samplingRate, setSamplingRate] = useState('5');
  const [enabled, setEnabled] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/groups').then(res => res.json()).then(setGroups);
  }, []);

  const loadTags = (groupId) => {
    fetch(`/api/tags/group/${groupId}`)
      .then(res => res.json())
      .then(setTags)
      .catch(() => setTags([]));
  };

  const handleGroupChange = (id) => {
    setGroupId(id);
    loadTags(id);
  };

  const handleAddTag = async () => {
    if (!alias || !nodeId || !groupId) {
      setError("Alias, Node ID, and Group must be selected.");
      return;
    }

    const payload = {
      group_id: parseInt(groupId),
      tags: [{
        alias,
        node_id: nodeId,
        data_type: dataType,
        sampling_rate: parseInt(samplingRate),
        enabled
      }]
    };

    const res = await fetch('/api/tags/batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(res => res.json());

    if (res.success) {
      setAlias('');
      setNodeId('');
      setSamplingRate('5');
      setEnabled(true);
      setError('');
      loadTags(groupId);
    } else {
      setError(res.detail || 'Failed to save tag');
    }
  };

  const handleDelete = async (id) => {
    await fetch(`/api/tags/${id}`, { method: 'DELETE' });
    loadTags(groupId);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Tag Manager</h1>

      <div className="bg-white p-4 rounded shadow-md mb-4 max-w-2xl">
        <div className="mb-2">
          <label className="block text-sm font-medium">Select Group</label>
          <select
            value={groupId}
            onChange={(e) => handleGroupChange(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          >
            <option value="">-- Choose Group --</option>
            {groups.map(g => (
              <option key={g.id} value={g.id}>{g.name}</option>
            ))}
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4 mt-4">
          <div>
            <label className="block text-sm font-medium">Alias</label>
            <input
              value={alias}
              onChange={(e) => setAlias(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
              placeholder="Unique tag alias"
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Node ID</label>
            <input
              value={nodeId}
              onChange={(e) => setNodeId(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
              placeholder="opc.tcp://.../NodeId"
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Data Type</label>
            <select
              value={dataType}
              onChange={(e) => setDataType(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
            >
              <option value="float">float</option>
              <option value="int">int</option>
              <option value="string">string</option>
              <option value="bool">bool</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium">Sampling Rate (s)</label>
            <input
              value={samplingRate}
              onChange={(e) => setSamplingRate(e.target.value)}
              type="number"
              min="1"
              className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
            />
          </div>
          <div className="col-span-2 flex items-center space-x-2 mt-2">
            <input
              type="checkbox"
              checked={enabled}
              onChange={(e) => setEnabled(e.target.checked)}
            />
            <label className="text-sm">Enable Tag</label>
          </div>
        </div>

        {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
        <button
          onClick={handleAddTag}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Add Tag
        </button>
      </div>

      <div className="max-w-2xl">
        <h2 className="text-xl font-semibold mb-2">Tags in Group</h2>
        {tags.length === 0 ? (
          <div className="text-gray-500">No tags found for this group.</div>
        ) : (
          <table className="w-full text-left border">
            <thead className="bg-gray-200">
              <tr>
                <th className="p-2">Alias</th>
                <th className="p-2">Node ID</th>
                <th className="p-2">Type</th>
                <th className="p-2">Rate</th>
                <th className="p-2">Enabled</th>
                <th className="p-2"></th>
              </tr>
            </thead>
            <tbody>
              {tags.map(tag => (
                <tr key={tag.id} className="border-t">
                  <td className="p-2">{tag.alias}</td>
                  <td className="p-2">{tag.node_id}</td>
                  <td className="p-2">{tag.data_type}</td>
                  <td className="p-2">{tag.sampling_rate}s</td>
                  <td className="p-2">{tag.enabled ? 'Yes' : 'No'}</td>
                  <td className="p-2">
                    <button
                      onClick={() => handleDelete(tag.id)}
                      className="text-red-600 hover:underline text-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
