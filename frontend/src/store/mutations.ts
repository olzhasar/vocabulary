import { MutationTree } from "vuex";
import { RootState } from "../types";
import apiClient from "../api_client";

export const mutations: MutationTree<RootState> = {
  setToken(store, payload) {
    store.token = payload.token;
    localStorage.setItem("token", payload.token);
    apiClient.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${payload.token}`;
  },
  setWords(store, payload) {
    store.words = payload.words;
  }
};
