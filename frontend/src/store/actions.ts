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

        apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;

        localStorage.setItem("token", token);
        store.commit("setToken", { token: token });

        router.push("/");
      })
      .catch(err => {
        let msg: string;

        if (err.response && err.response.status === 422) {
          msg = "Invalid credentials";
        } else {
          msg = "Server error. Please, try later";
        }

        localStorage.removeItem("token");
        store.commit("authError", { msg: msg });
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
  },

  getWords(store) {
    apiClient.get("/words").then(response => {
      const words = response.data.words;

      store.commit("setWords", { words: words });
    });
  }
};
