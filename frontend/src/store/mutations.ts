import { MutationTree } from "vuex";
import { RootState } from "../types";

export const mutations: MutationTree<RootState> = {
  setToken(store, payload) {
    store.token = payload.token;
  },
  authError(store, payload) {
    store.token = null;
    store.authError = payload.msg;
  },
  setWords(store, payload) {
    store.words = payload.words;
  }
};
