import { createStore } from 'vuex';
import userModule from './user';

export default createStore({
  state() {
    return {
      // state 属性
    };
  },
  mutations: {
    // mutations
  },
  actions: {
    clear({ commit }) {
      commit("$_removeStorage");
    }
  },
  modules: {
    user: userModule
  }
});