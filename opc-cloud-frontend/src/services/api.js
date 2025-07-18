const API_BASE = '/api';

export const fetchServers = () =>
  fetch(`${API_BASE}/servers`).then(res => res.json());

export const addServer = (name, endpoint_url) =>
  fetch(`${API_BASE}/servers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, endpoint_url })
  }).then(res => res.json());

export const deleteServer = (id) =>
  fetch(`${API_BASE}/servers/${id}`, { method: 'DELETE' }).then(res => res.json());

export const fetchGroups = () =>
  fetch(`${API_BASE}/groups`).then(res => res.json());

export const fetchTags = (groupId) =>
  fetch(`${API_BASE}/tags/group/${groupId}`).then(res => res.json());

export const addTags = (group_id, tags) =>
  fetch(`${API_BASE}/tags/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ group_id, tags })
  }).then(res => res.json());

export const deleteTag = (id) =>
  fetch(`${API_BASE}/tags/${id}`, { method: 'DELETE' }).then(res => res.json());
