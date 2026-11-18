const API_ROOT = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const authHeaders = () => {
  const token = localStorage.getItem("interview_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

async function handle(res) {
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body.error || body.detail || `Request failed (${res.status})`);
  return body;
}
async function request(path, options = {}) {
  return handle(await fetch(`${API_ROOT}${path}`, { ...options, headers: { ...authHeaders(), ...options.headers } }));
}
export const register = (data) => request("/api/auth/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
export const login = (data) => request("/api/auth/login", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
export const createSession = (data) => request("/api/sessions", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
export const getQuestions = (id) => request(`/api/sessions/${id}/questions`);
export const submitAnswer = (sessionId, questionId, answerText) => request(`/api/sessions/${sessionId}/questions/${questionId}/answers`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ answerText }) });
export const getSummary = (id) => request(`/api/sessions/${id}/summary`);
export const getHistory = () => request("/api/sessions");
export const getEvaluationDashboard = () => request("/api/evaluations/dashboard");
export const saveHumanReview = (data) => request("/api/evaluations", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
export async function extractResume(file) {
  const form = new FormData(); form.append("file", file);
  return request("/api/resume/extract", { method: "POST", body: form });
}
