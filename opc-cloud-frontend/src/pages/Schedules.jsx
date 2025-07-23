
import { useEffect, useState } from 'react';

export default function Schedules() {
  const [groups, setGroups] = useState([]);
  const [schedules, setSchedules] = useState([]);
  const [groupId, setGroupId] = useState('');
  const [format, setFormat] = useState('pdf');
  const [scheduleType, setScheduleType] = useState('Daily');
  const [outputFolder, setOutputFolder] = useState('');
  const [template, setTemplate] = useState(null);
  const [isEnabled, setIsEnabled] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/groups/').then(res => res.json()).then(setGroups);
    fetch('/api/reports/').then(res => res.json()).then(setSchedules);
  }, []);

  const handleAdd = async () => {
    if (!groupId || !format || !scheduleType || !outputFolder) {
      setError("All fields except template are required.");
      return;
    }

    const formData = new FormData();
    formData.append("group_id", groupId);
    formData.append("format", format);
    formData.append("schedule_type", scheduleType);
    formData.append("output_folder", outputFolder);
    formData.append("is_enabled", isEnabled);
    if (template) {
      formData.append("template", template);
    }

    const response = await fetch('/api/reports/schedules', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      setGroupId('');
      setFormat('pdf');
      setScheduleType('Daily');
      setOutputFolder('');
      setTemplate(null);
      setIsEnabled(true);
      setError('');
      fetch('/api/reports/').then(res => res.json()).then(setSchedules);
    } else {
      const err = await response.json();
      setError(err.detail || 'Failed to add schedule');
    }
  };

  const handleDelete = async (id) => {
    await fetch(`/api/reports/schedules/${id}`, { method: 'DELETE' });
    fetch('/api/reports/').then(res => res.json()).then(setSchedules);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Scheduled Reports</h1>

      <div className="bg-white p-4 rounded shadow-md mb-6 max-w-xl space-y-3">
        <div>
          <label className="block text-sm font-medium">Select Group</label>
          <select
            value={groupId}
            onChange={(e) => setGroupId(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          >
            <option value="">-- Choose Group --</option>
            {groups.map((g) => (
              <option key={g.id} value={g.id}>{g.name}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Format</label>
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          >
            <option value="pdf">PDF</option>
            <option value="excel">Excel</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Schedule Type</label>
          <select
            value={scheduleType}
            onChange={(e) => setScheduleType(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          >
            <option value="Daily">Daily</option>
            <option value="Weekly">Weekly</option>
            <option value="Monthly">Monthly</option>
            <option value="SpecificTime">Specific Time</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Output Folder</label>
          <input
            value={outputFolder}
            onChange={(e) => setOutputFolder(e.target.value)}
            placeholder="e.g. /reports/daily/"
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          />
        </div>

        <div>
          <label className="block text-sm font-medium">Excel Template (optional)</label>
          <input
            type="file"
            accept=".xlsx"
            onChange={(e) => setTemplate(e.target.files[0])}
            className="w-full mt-1"
          />
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={isEnabled}
            onChange={(e) => setIsEnabled(e.target.checked)}
          />
          <label className="text-sm">Enabled</label>
        </div>

        {error && <div className="text-red-600 text-sm">{error}</div>}

        <button
          onClick={handleAdd}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Add Schedule
        </button>
      </div>

      <div className="max-w-xl">
        <h2 className="text-xl font-semibold mb-2">Current Schedules</h2>
        {schedules.length === 0 ? (
          <div className="text-gray-500">No schedules defined.</div>
        ) : (
          <ul className="space-y-2">
            {schedules.map((s) => (
              <li key={s.id} className="flex justify-between items-center bg-gray-100 p-3 rounded">
                <div>
                  <div className="font-medium">Group: {s.group_id} | {s.schedule_type}</div>
                  <div className="text-sm text-gray-600">{s.output_folder} ({s.format})</div>
                </div>
                <button
                  onClick={() => handleDelete(s.id)}
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
