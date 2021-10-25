const state = {
    authState: undefined
};

const getters = {
    authState: state => state.authState
};

const mutations = {
    authState: (state, authState) => {
        if (authState) {
            state.authState = authState
        } else {
            state.authState = undefined;
        }
    }
};

const actions = {
    setAuthState: (context, authState) => {
        context.commit('authState', authState);
    }
};

export default {
    state,
    mutations,
    getters,
    actions
}
