const state = {
    managedAccounts: undefined
};

const getters = {
    managedAccounts: state => state.managedAccounts
};

const mutations = {
    managedAccounts: (state, managedAccounts) => {
        if (managedAccounts) {
            state.managedAccounts = managedAccounts
        } else {
            state.managedAccounts = undefined;
        }
    }
};

const actions = {
    setManagedAccounts: (context, managedAccounts) => {
        context.commit('managedAccounts', managedAccounts);
    }
};

export default {
    state,
    mutations,
    getters,
    actions
}
