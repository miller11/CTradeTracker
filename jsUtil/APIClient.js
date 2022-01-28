import axios from 'axios';
import {store} from '@/store/store'

const BASE_URL = 'https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/';

class ApiClient {
    getJWTToken() {
        return store.getters.currentUser.signInUserSession.idToken.jwtToken;
    }

    authHeaders() {
        return {
            headers: {
                Authorization: this.getJWTToken()
            }
        }
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
        return axios.post(BASE_URL + 'api-key', data,  this.authHeaders());
    }

    getAPIKeyStatus() {
        return axios.get(BASE_URL + 'api-key', this.authHeaders())
    }

    getAccounts() {
        return axios.get(BASE_URL + 'accounts', this.authHeaders())
    }

    getAccountGraph(accountId) {
        return axios.get(BASE_URL + 'account-graph/' + accountId, this.authHeaders())
    }

    getTradeGraph(accountId) {
        return axios.get(BASE_URL + 'trade-graph/' + accountId, this.authHeaders())
    }

    getTransactions(accountId) {
        return axios.get(BASE_URL + 'transactions/' + accountId, this.authHeaders())
    }

    getBotDecisions(accountId) {
        return axios.get(BASE_URL + 'bot-decisions/' + accountId, this.authHeaders())
    }

    getCBPAccount(accountId) {
        return axios.get(BASE_URL + 'cbp-account/' + accountId, this.authHeaders())
    }

    getCBPAccounts() {
        return axios.get(BASE_URL + 'cbp-accounts/', this.authHeaders())
    }

    addCBPAccount(account_id, data) {
        return axios.post(BASE_URL + 'cbp-accounts/' + account_id, data, this.authHeaders());
    }

    removeCBPAccount(account_id) {
        return axios.delete(BASE_URL + 'cbp-accounts/' + account_id, this.authHeaders());
    }
}

export default ApiClient;
