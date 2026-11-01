
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Add JWT token to protected requests.
api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export const loginUser = async (email, password) => {
  const form = new URLSearchParams();

  form.append("username", email);
  form.append("password", password);

  const response = await api.post("/auth/login", form, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  sessionStorage.setItem(
    "access_token",
    response.data.access_token
  );

  return response.data;
};

export const getProfile = () => api.get("/auth/me");

export const getCompany = () => api.get("/companies/me");

export const getContacts = () => api.get("/contacts");

export const getReports = () =>
  api.get("/reports/notifications");

export const getSummary = () => api.get("/reports/summary");

export const createContact = (data) =>
  api.post("/contacts", data);

export const sendSMS = (contact_id, message) =>
  api.post("/sms/send", { contact_id, message });

export const startCall = (contact_id) =>
  api.post("/calls/start", { contact_id });

export const logout = () => {
  sessionStorage.removeItem("access_token");
};

export default api;
