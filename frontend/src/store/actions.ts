import { ActionTree } from "vuex";
import apiClient from "../api_client";
import { RootState } from "../types";
import router from "../router";

export const actions: ActionTree<RootState, any> = {
  login(store, payload) {
    const formData = new FormData();
    formData.append("username", payload.email);
    formData.append("password", payload.password);

    apiClient
      .post("/token", formData)
      .then(response => {
        const token = response.data.access_token;

        localStorage.setItem("token", token);
        apiClient.defaults.headers.common["Authorization"] = token + " Bearer";
        store.state.token = response.data.access_token;

        router.push("/");
      })
      .catch(err => {
        if (err.response && err.response.status === 422) {
          store.state.authError = "Invalid credentials";
        } else {
          store.state.authError = "Server error. Please, try later";
        }
      });
  },

  signup(store, payload) {
    apiClient
      .post("/signup", {
        username: payload.username,
        password: payload.password,
        repeatPassword: payload.repeatPassword
      })
      .then(response => (store.state.token = response.data.access_token));
  }
};
