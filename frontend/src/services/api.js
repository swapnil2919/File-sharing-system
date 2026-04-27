import axios from "axios";

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const API = axios.create({
  baseURL: API_BASE_URL
});

export const uploadFile = (formData) => {
  return API.post("/upload", formData);
};

export const downloadFile = (hash) => {
  return API.get(`/download/${hash}`, {
    responseType: "blob",
  });
};
