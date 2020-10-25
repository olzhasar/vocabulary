import { ActionTree } from "vuex";
import apiClient from "../api_client";
import { RootState } from "../types";

export const actions: ActionTree<RootState, any> = {
  login(store, payload) {
    return new Promise((resolve, reject) => {
      const formData = new FormData();
      formData.append("username", payload.email);
      formData.append("password", payload.password);

      apiClient
        .post("/token", formData)
        .then(response => {
          const token = response.data.access_token;
          store.commit("setToken", { token: token });

          resolve();
        })
        .catch(err => {
          if (err.response && err.response.status === 401) {
            reject("Invalid credentials");
          } else {
            reject("Unexpected server error. Please, try later");
          }
        });
    });
  },

  signup(store, payload) {
    return new Promise((resolve, reject) => {
      apiClient
        .post("/signup", {
          email: payload.email,
          password: payload.password,
          repeat_password: payload.repeatPassword // eslint-disable-line
        })
        .then(response => {
          const token = response.data.access_token;

          store.commit("setToken", { token: token });

          resolve();
        })
        .catch(err => {
          if (err.response && err.response.status === 409) {
            reject("This email is already registered. Please, login instead");
          } else {
            reject("Unexpected server error. Please, try later");
          }
        });
    });
  },

  getWords(store) {
    apiClient.get("/words").then(response => {
      const words = response.data.words;

      store.commit("setWords", { words: words });
    });
  }
};
