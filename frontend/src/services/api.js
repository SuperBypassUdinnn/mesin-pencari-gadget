import axios from "axios";

const API_BASE = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

export const searchGadgets = async (params) => {
  const { data } = await api.get("/search", { params });
  return data;
};

export const getDocument = async (id) => {
  const { data } = await api.get(`/documents/${encodeURIComponent(id)}`);
  return data;
};

export const getHealth = async () => {
  const { data } = await api.get("/health");
  return data;
};

export const getEvaluation = async () => {
  const { data } = await api.get("/evaluation");
  return data;
};

export default { searchGadgets, getDocument, getHealth, getEvaluation };
