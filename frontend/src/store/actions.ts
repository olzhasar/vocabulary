import { ActionTree } from "vuex";
import apiClient from "../api_client";
import { RootState } from "../types";

export const actions: ActionTree<RootState, any> = {
  login(store, payload) {
    const formData = new FormData();
    formData.append("username", payload.email);
    formData.append("password", payload.password);

    apiClient
      .post("/token", formData)
      .then(response => (store.state.token = response.data.access_token));
  }
};
