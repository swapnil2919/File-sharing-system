import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000"
});

export const uploadFile = (formData) => {
  return API.post("/upload", formData);
};

export const downloadFile = (hash) => {
  return API.get(`/download/${hash}`, {
    responseType: "blob",
  });
};
