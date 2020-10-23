import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 5000
});

const token = localStorage.getItem("token");

if (token) {
  apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export default apiClient;
