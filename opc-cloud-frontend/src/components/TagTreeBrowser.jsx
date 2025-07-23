
import { useEffect, useState } from 'react';

export default function TagTreeBrowser({ serverId, onTagSelect }) {
  const [tree, setTree] = useState([]);
  const [expanded, setExpanded] = useState({});

  useEffect(() => {
    if (serverId) fetchChildren(null, setTree);
  }, [serverId]);

  const fetchChildren = async (nodeId, setFn) => {
    const path = nodeId ? `/api/servers/${serverId}/browse/${encodeURIComponent(nodeId)}` : `/api/servers/${serverId}/browse`;
    const res = await fetch(path).then(r => r.json()).catch(() => []);
    setFn(res);
  };

  const toggleNode = async (node) => {
    if (expanded[node.node_id]) {
      setExpanded(prev => ({ ...prev, [node.node_id]: false }));
    } else {
      const res = await fetch(`/api/servers/${serverId}/browse/${encodeURIComponent(node.node_id)}`).then(r => r.json()).catch(() => []);
      setExpanded(prev => ({ ...prev, [node.node_id]: res }));
    }
  };

  const renderNode = (node, depth = 0) => {
    const hasChildren = node.has_children;
    const isExpanded = expanded[node.node_id];

    return (
      <div key={node.node_id} className="pl-4">
        <div className="flex items-center space-x-2">
          {hasChildren && (
            <button onClick={() => toggleNode(node)} className="text-xs text-blue-600 underline">
              {isExpanded ? '-' : '+'}
            </button>
          )}
          {!hasChildren && (
            <input type="checkbox" onChange={() => onTagSelect(node)} />
          )}
          <span className="text-sm">{node.display_name}</span>
        </div>
        {Array.isArray(isExpanded) && isExpanded.map(child => renderNode(child, depth + 1))}
      </div>
    );
  };

  return (
    <div className="bg-white p-4 rounded shadow-md overflow-y-auto max-h-[500px]">
      <h2 className="text-lg font-semibold mb-2">Browse Tags</h2>
      {tree.length === 0 ? (
        <div className="text-gray-500 text-sm">No data to display.</div>
      ) : (
        tree.map(node => renderNode(node))
      )}
    </div>
  );
}
