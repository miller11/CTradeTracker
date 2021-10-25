const state = {
    currentUser: undefined
};

const getters = {
    currentUser: state => state.currentUser
};

const mutations = {
    userStatus: (state, user) => {
        if (user) {
            state.currentUser = user
        } else {
            state.currentUser = undefined;
        }
    }
};

const actions = {
    setUser: (context, user) => {
        context.commit('userStatus', user);
    }
};


export default {
    state,
    mutations,
    getters,
    actions
}
