import { ActionTree } from "vuex";
import apiClient from "../api_client";
import { RootState } from "../types";

export const actions: ActionTree<RootState, any> = {
  login(store, payload) {
    apiClient
      .post("/token", { username: payload.email, password: payload.password })
      .then(response => (store.state.token = response.data.access_token));
  }
};
