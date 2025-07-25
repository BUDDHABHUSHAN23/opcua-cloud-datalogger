// import { useEffect, useState } from 'react';

// export default function TagTreeBrowser({ serverId, onTagSelect }) {
//   const [tree, setTree] = useState([]);
//   const [expandedNodes, setExpandedNodes] = useState({});
//   const [loadingNodes, setLoadingNodes] = useState({});

//   useEffect(() => {
//     if (serverId) {
//       fetch(`/api/servers/${serverId}/browse`)
//         .then(res => res.json())
//         .then(setTree)
//         .catch(err => console.error("Failed to load root nodes", err));
//     } else {
//       setTree([]);
//     }
//   }, [serverId]);

//   const fetchChildren = async (nodeId) => {
//     setLoadingNodes(prev => ({ ...prev, [nodeId]: true }));
//     try {
//       const res = await fetch(`/api/servers/${serverId}/browse/${encodeURIComponent(nodeId)}`);
//       const children = await res.json();
//       setTree(prev => updateTreeWithChildren(prev, nodeId, children));
//       setExpandedNodes(prev => ({ ...prev, [nodeId]: true }));
//     } catch (err) {
//       console.error("Error fetching children", err);
//     } finally {
//       setLoadingNodes(prev => ({ ...prev, [nodeId]: false }));
//     }
//   };

//   const updateTreeWithChildren = (nodes, parentId, children) => {
//     return nodes.map(n => {
//       if (n.nodeId === parentId) {
//         return { ...n, children };
//       } else if (n.children) {
//         return { ...n, children: updateTreeWithChildren(n.children, parentId, children) };
//       }
//       return n;
//     });
//   };

//   const renderNode = (node, level = 0) => {
//     const isFolder = node.nodeClass === 'Object' || node.nodeClass === 'Folder';
//     const isExpanded = expandedNodes[node.nodeId];
//     const isLoading = loadingNodes[node.nodeId];

//     return (
//       <div key={node.nodeId} style={{ marginLeft: level * 16 }} className="mb-1">
//         {isFolder && (
//           <button
//             onClick={() => fetchChildren(node.nodeId)}
//             className="mr-1 text-blue-600 hover:underline"
//           >
//             {isExpanded ? '▼' : '▶'}
//           </button>
//         )}

//         {!isFolder && (
//           <input
//             type="checkbox"
//             className="mr-2"
//             onChange={() => onTagSelect({
//               node_id: node.nodeId,
//               display_name: node.displayName
//             })}
//           />
//         )}

//         {node.displayName} {isLoading && <span className="text-gray-400 text-xs">(loading...)</span>}

//         {isExpanded && node.children && (
//           <div>{node.children.map(child => renderNode(child, level + 1))}</div>
//         )}
//       </div>
//     );
//   };

//   return (
//     <div className="p-4 border rounded bg-white max-h-[500px] overflow-y-auto">
//       <h2 className="text-lg font-semibold mb-2">Browse Tags</h2>
//       {tree.length === 0 ? (
//         <div className="text-gray-500 text-sm">Select a server to start browsing</div>
//       ) : (
//         tree.map(node => renderNode(node))
//       )}
//     </div>
//   );
// }
import { useEffect, useState } from 'react';

export default function TagTreeBrowser({ serverId, onTagSelect }) {
  const [tree, setTree] = useState([]);
  const [expandedNodes, setExpandedNodes] = useState({});
  const [loadingNodes, setLoadingNodes] = useState({});

  useEffect(() => {
    if (serverId) {
      fetch(`/api/servers/${serverId}/browse`)
        .then(res => res.json())
        .then(setTree)
        .catch(err => console.error("Failed to load root nodes", err));
    } else {
      setTree([]);
    }
  }, [serverId]);

  const fetchChildren = async (nodeId) => {
    setLoadingNodes(prev => ({ ...prev, [nodeId]: true }));
    try {
      const res = await fetch(`/api/servers/${serverId}/browse/${encodeURIComponent(nodeId)}`);
      const children = await res.json();
      setTree(prev => updateTreeWithChildren(prev, nodeId, children));
      setExpandedNodes(prev => ({ ...prev, [nodeId]: true }));
    } catch (err) {
      console.error("Error fetching children", err);
    } finally {
      setLoadingNodes(prev => ({ ...prev, [nodeId]: false }));
    }
  };

  const updateTreeWithChildren = (nodes, parentId, children) => {
    return nodes.map(n => {
      if (n.nodeId === parentId) {
        return { ...n, children };
      } else if (n.children) {
        return { ...n, children: updateTreeWithChildren(n.children, parentId, children) };
      }
      return n;
    });
  };

  const renderNode = (node, level = 0) => {
    const isFolder = node.nodeClass === 'Object' || node.nodeClass === 'Folder';
    const isExpanded = expandedNodes[node.nodeId];
    const isLoading = loadingNodes[node.nodeId];

    return (
      <div key={node.nodeId} style={{ marginLeft: level * 16 }} className="mb-1">
        {isFolder && (
          <button
            onClick={() => fetchChildren(node.nodeId)}
            className="mr-1 text-blue-600 hover:underline"
          >
            {isExpanded ? '▼' : '▶'}
          </button>
        )}

        {!isFolder && (
          <input
            type="checkbox"
            className="mr-2"
            onChange={() => onTagSelect({
              node_id: node.nodeId,
              display_name: node.displayName
            })}
          />
        )}

        {node.displayName} {isLoading && <span className="text-gray-400 text-xs">(loading...)</span>}

        {isExpanded && node.children && (
          <div>{node.children.map(child => renderNode(child, level + 1))}</div>
        )}
      </div>
    );
  };

  return (
    <div className="p-4 border rounded bg-white max-h-[500px] overflow-y-auto">
      <h2 className="text-lg font-semibold mb-2">Browse Tags</h2>
      {tree.length === 0 ? (
        <div className="text-gray-500 text-sm">Select a server to start browsing</div>
      ) : (
        tree.map(node => renderNode(node))
      )}
    </div>
  );
}
