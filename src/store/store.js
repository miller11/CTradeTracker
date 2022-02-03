import Vue from 'vue'
import Vuex from 'vuex'

import user from './modules/user'
import authState from './modules/authState'
import managedAccounts from "./modules/managedAccounts";

Vue.use(Vuex);

export const store = new Vuex.Store({
    modules: {
        user,authState,managedAccounts
    }
});
