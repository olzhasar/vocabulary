import axios from "axios";
import router from "../router";
import store from "../store";

const apiClient = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 5000
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
      store.commit("removeToken");
      router.push("/login");
    } else {
      throw error;
    }
  }
);

export default apiClient;
