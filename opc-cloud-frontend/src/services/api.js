const API_BASE =
  import.meta.env.DEV ? '/api' : import.meta.env.VITE_API_BASE_URL + '/api';

export const fetchServers = async () => {
  const res = await fetch(`${API_BASE}/servers/`);
  if (!res.ok) throw new Error("Failed to fetch servers");
  return res.json();
};

export const addServer = async (name, endpoint_url) => {
  const res = await fetch(`${API_BASE}/servers/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, endpoint_url }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Failed to add server");
  return { success: true, ...data };
};

export const deleteServer = (id) =>
  fetch(`${API_BASE}/servers/${id}/`, { method: 'DELETE' }).then(res => res.json());

export const fetchGroups = () =>
  fetch(`${API_BASE}/groups/`).then(res => res.json());

export const fetchTags = (groupId) =>
  fetch(`${API_BASE}/tags/group/${groupId}/`).then(res => res.json());

export const addTags = (group_id, tags) =>
  fetch(`${API_BASE}/tags/batch/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ group_id, tags })
  }).then(res => res.json());

export const deleteTag = (id) =>
  fetch(`${API_BASE}/tags/${id}/`, { method: 'DELETE' }).then(res => res.json());