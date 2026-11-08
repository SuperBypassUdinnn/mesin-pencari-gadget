import axios from "axios";

const API_BASE = "http://localhost:8000/api";

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

export const searchGadgets = async (params) => {
  const { data } = await apiClient.get("/search", { params });
  return data;
};

export const getDocument = async (id) => {
  const { data } = await apiClient.get(`/documents/${encodeURIComponent(id)}`);
  return data;
};

export const getHealth = async () => {
  const { data } = await apiClient.get("/health");
  return data;
};

export const getEvaluation = async () => {
  const { data } = await apiClient.get("/evaluation");
  return data;
};

export const api = { searchGadgets, getDocument, getHealth, getEvaluation };
export default api;
