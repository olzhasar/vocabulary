import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import { RootState } from "../types";

import { actions } from "./actions";
import { mutations } from "./mutations";

Vue.use(Vuex);

const store: StoreOptions<RootState> = {
  state: {
    token: localStorage.getItem("token"),
    authError: null,
    words: []
  },
  actions: actions,
  mutations: mutations,
  getters: {
    isLoggedIn: state => !!state.token
  }
};

export default new Vuex.Store(store);
