import { useAuth } from '../context/AuthContext';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api/v1';

/**
 * Core fetch wrapper that automatically attaches the Firebase ID token.
 */
const apiFetch = async (endpoint, options = {}) => {
  const { auth } = await import('../config/firebase');
  const user = auth.currentUser;

  let token = null;
  if (user) {
    token = await user.getIdToken();
  }

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Parse JSON regardless of ok status so we get error messages
  let data;
  try {
    data = await response.json();
  } catch {
    data = { error: 'Invalid server response', message: response.statusText };
  }

  if (!response.ok) {
    const err = new Error(data.message || data.error || 'API request failed');
    err.status = response.status;
    err.data = data;
    throw err;
  }

  return data;
};

// ─── Problems API ─────────────────────────────────────────────────────────────

export const problemsApi = {
  list: () => apiFetch('/problems'),
  get: (id) => apiFetch(`/problems/${id}`),
  create: (payload) => apiFetch('/problems', { method: 'POST', body: JSON.stringify(payload) }),
  update: (id, payload) => apiFetch(`/problems/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  delete: (id) => apiFetch(`/problems/${id}`, { method: 'DELETE' }),
  getTestCases: (id) => apiFetch(`/problems/${id}/testcases`),
};

// ─── Submissions API ──────────────────────────────────────────────────────────

export const submissionsApi = {
  run: (payload) => apiFetch('/submissions/run', { method: 'POST', body: JSON.stringify(payload) }),
  submit: (payload) => apiFetch('/submissions/submit', { method: 'POST', body: JSON.stringify(payload) }),
  list: (lastDocId = null) => {
    const qs = lastDocId ? `?lastDocId=${lastDocId}` : '';
    return apiFetch(`/submissions${qs}`);
  },
  get: (id) => apiFetch(`/submissions/${id}`),
};

// ─── Dashboard API ────────────────────────────────────────────────────────────

export const dashboardApi = {
  stats: () => apiFetch('/dashboard/stats'),
};

// ─── Admin APIs ───────────────────────────────────────────────────────────────

export const adminApi = {
  // Analytics
  getAnalytics: () => apiFetch('/admin/analytics'),
  // Users
  listUsers: () => apiFetch('/admin/users'),
  suspendUser: (uid) => apiFetch(`/admin/users/${uid}/suspend`, { method: 'POST' }),
  reinstateUser: (uid) => apiFetch(`/admin/users/${uid}/reinstate`, { method: 'POST' }),
  // Submissions explorer
  listSubmissions: (filters = {}) => {
    const qs = new URLSearchParams(filters).toString();
    return apiFetch(`/admin/submissions${qs ? `?${qs}` : ''}`);
  },
  // AI Prompts
  listPrompts: () => apiFetch('/admin/prompts'),
  createPrompt: (payload) => apiFetch('/admin/prompts', { method: 'POST', body: JSON.stringify(payload) }),
  updatePrompt: (id, payload) => apiFetch(`/admin/prompts/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  deletePrompt: (id) => apiFetch(`/admin/prompts/${id}`, { method: 'DELETE' }),
};

export default apiFetch;
