import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor — add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor — handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.error?.message ||
      error.response?.data?.message ||
      error.message ||
      "An unexpected error occurred";
    return Promise.reject(new Error(message));
  }
);

/**
 * Upload a leaf image for disease prediction.
 */
export async function predictDisease(imageFile, language = "en") {
  const formData = new FormData();
  formData.append("file", imageFile);
  formData.append("language", language);

  const response = await api.post("/api/v1/predict", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}

/**
 * Get list of supported crops.
 */
export async function getCrops() {
  const response = await api.get("/api/v1/crops");
  return response.data;
}

/**
 * Get disease info by ID.
 */
export async function getDiseaseInfo(diseaseId, language = "en") {
  const response = await api.get(`/api/v1/diseases/${diseaseId}`, {
    params: { language },
  });
  return response.data;
}

/**
 * Health check.
 */
export async function healthCheck() {
  const response = await api.get("/api/health");
  return response.data;
}

export default api;
