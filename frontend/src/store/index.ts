import Vue from "vue";
import Vuex, { StoreOptions } from "vuex";
import { RootState } from "../types";

import { actions } from "./actions";

Vue.use(Vuex);

const store: StoreOptions<RootState> = {
  state: {
    token: localStorage.getItem("token"),
    words: []
  },
  actions: actions
};

export default new Vuex.Store(store);
