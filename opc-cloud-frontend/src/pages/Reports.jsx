
import { useEffect, useState } from 'react';

export default function Reports() {
  const [groups, setGroups] = useState([]);
  const [groupId, setGroupId] = useState('');
  const [format, setFormat] = useState('pdf');
  const [layout, setLayout] = useState('row');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [templateFile, setTemplateFile] = useState(null);
  const [error, setError] = useState('');
  const [downloadUrl, setDownloadUrl] = useState('');

  useEffect(() => {
    fetch('/api/groups/').then(res => res.json()).then(setGroups);
  }, []);

  const handleGenerate = async () => {
    if (!groupId || !start || !end || !format) {
      setError("All fields except template are required.");
      return;
    }

    const formData = new FormData();
    formData.append("group_id", groupId);
    formData.append("format", format);
    formData.append("start_dt", start);
    formData.append("end_dt", end);
    formData.append("layout", layout);
    if (templateFile) {
      formData.append("template", templateFile);
    }

    const response = await fetch('/api/reports/generate', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);
      setError('');
    } else {
      const err = await response.json();
      setError(err.detail || 'Report generation failed');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Generate Report</h1>

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
          <label className="block text-sm font-medium">Start Date/Time</label>
          <input
            type="datetime-local"
            value={start}
            onChange={(e) => setStart(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          />
        </div>

        <div>
          <label className="block text-sm font-medium">End Date/Time</label>
          <input
            type="datetime-local"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          />
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
          <label className="block text-sm font-medium">Layout (Excel only)</label>
          <select
            value={layout}
            onChange={(e) => setLayout(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mt-1"
          >
            <option value="row">Timestamps as Rows</option>
            <option value="col">Timestamps as Columns</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Excel Template (optional)</label>
          <input
            type="file"
            accept=".xlsx"
            onChange={(e) => setTemplateFile(e.target.files[0])}
            className="w-full mt-1"
          />
        </div>

        {error && <div className="text-red-600 text-sm">{error}</div>}

        <button
          onClick={handleGenerate}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Generate Report
        </button>

        {downloadUrl && (
          <div className="mt-4">
            <a
              href={downloadUrl}
              download={`report.${format === 'pdf' ? 'pdf' : 'xlsx'}`}
              className="text-green-700 underline"
            >
              Click to download report
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
