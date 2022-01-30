import axios from 'axios';
import {store} from '@/store/store'
import Vue from 'vue'



class ApiClient {
    constructor() {
        let jwt = ''

        if(store.getters.currentUser !== undefined) {
            jwt = store.getters.currentUser.signInUserSession.idToken.jwtToken
        }

        this.api = axios.create({
            baseURL: 'https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/',
            timeout: 60000,
            headers: {'Authorization': jwt}
        });

        this.api.interceptors.response.use((response) => response, (error) => {
            console.log(error)
            let message = 'An Error occurred.'

            if(error.response !== undefined && error.response.data !== undefined) {
                message = error.response.data
            }

            Vue.notify({
                group: 'default',
                position: 'bottom right',
                type: 'error',
                title: 'Error!',
                text: message
            })
        });
    }

    // wrapper for axios.all()
    all(requests) {
        return axios.all(requests);
    }

    // wrapper for axios.spread()
    spread(cb) {
        return axios.spread(cb);
    }

    setAPIKey(data) {
        return this.api.post('api-key/', data);
    }

    getAPIKeyStatus() {
        return this.api.get('api-key/')
    }

    getAccounts() {
        return this.api.get('accounts/')
    }

    getAccountGraph(accountId) {
        return this.api.get('account-graph/' + accountId)
    }

    getTradeGraph(accountId) {
        return this.api.get('trade-graph/' + accountId)
    }

    getTransactions(accountId) {
        return this.api.get('transactions/' + accountId)
    }

    getBotDecisions(accountId) {
        return this.api.get('bot-decisions/' + accountId)
    }

    getCBPAccount(accountId) {
        return this.api.get('cbp-account/' + accountId)
    }

    getCBPAccounts() {
        return this.api.get('cbp-accounts/')
    }

    addCBPAccount(account_id, data) {
        return this.api.post('cbp-accounts/' + account_id, data);
    }

    removeCBPAccount(account_id) {
        return this.api.delete('cbp-accounts/' + account_id);
    }
}

export default ApiClient;
