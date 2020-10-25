import axios from "axios";
import { AxiosTransformer } from "axios";
import router from "../router";
import humps from "humps";

const apiClient = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 5000,
  transformResponse: [
    ...(axios.defaults.transformResponse as AxiosTransformer[]),
    data => humps.camelizeKeys(data)
  ],
  transformRequest: [
    data => humps.decamelizeKeys(data),
    ...(axios.defaults.transformRequest as AxiosTransformer[])
  ]
});

const token = localStorage.getItem("token");

if (token) {
  apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

apiClient.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    if (error.response.status === 401) {
      router.push("/login");
    } else {
      throw error;
    }
  }
);

export default apiClient;
