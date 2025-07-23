
export const browseRootNodes = async (serverId) => {
  return await fetch(`/api/servers/${serverId}/browse/`).then(res => res.json());
};

export const browseChildren = async (serverId, nodeId) => {
  return await fetch(`/api/servers/${serverId}/browse/${encodeURIComponent(nodeId)}`).then(res => res.json());
};
