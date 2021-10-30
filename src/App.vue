<template>
  <div id="app">
    <div>
      <div>
        <b-navbar toggleable="sm" type="dark" variant="dark">
          <b-navbar-brand href="#">TradeTracker</b-navbar-brand>

          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

          <b-collapse id="nav-collapse" v-if="isSignedIn" is-nav>
            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
              <b-nav-item-dropdown text="Select Account" right>
                <b-dropdown-item v-for="(account) in accounts" :key="account.account_id"
                                 @click="activeAccount = account;">{{ account.name }}
                </b-dropdown-item>
              </b-nav-item-dropdown>

              <b-nav-item href="#" v-if="activeAccount !== undefined" disabled>{{ activeAccount.name }}</b-nav-item>


              <b-nav-item-dropdown right>
                <!-- Using 'button-content' slot -->
                <template #button-content>
                  <em>{{ currentUser.attributes.email }}</em>
                </template>
                <b-dropdown-item @click="appSignOut()">Sign Out</b-dropdown-item>
              </b-nav-item-dropdown>
            </b-navbar-nav>
          </b-collapse>
        </b-navbar>
      </div>
      <amplify-authenticator username-alias="email"></amplify-authenticator>


    </div>

    <div class="container mt-4">
      <!-- Content here -->
      <div v-if="activeAccount !== undefined">
        <ul class="nav nav-tabs">
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeNavTab === NavTab.TRADE_GRAPH }"
               @click="activeNavTab = NavTab.TRADE_GRAPH">Trade(s)</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeNavTab === NavTab.GAIN_LOSS }"
               @click="activeNavTab = NavTab.GAIN_LOSS">Gain/Loss</a>
          </li>
        </ul>

        <div class="row">
          <div class="col-12">
            <div v-if="dataLoading" class="row">
              <b-spinner variant="success" label="Loading"></b-spinner>
            </div>
            <div id="graph"></div>
          </div>
        </div>

        <div class="row" v-if="transactions !== undefined">
          <div class="col-12">
            <h3>Transactions</h3>
            <b-table striped hover :items="transactions" :fields="transactions_fields" sort-by="timestamp" sort-desc="true"></b-table>
          </div>
        </div>

        <div class="row" v-if="botDecisions !== undefined">
          <div class="col-12">
            <h3>Bot Decisions</h3>
            <b-table striped hover :items="botDecisions" :fields="bot_decision_fields" sort-by="timestamp" sort-desc="true"></b-table>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>


<script>

import {onAuthUIStateChange} from '@aws-amplify/ui-components'
import {Auth} from 'aws-amplify';
import {store} from './store/store';
import axios from 'axios'

import Plotly from 'plotly.js-dist'

const NavTab = {
  TRADE_GRAPH: 0,
  GAIN_LOSS: 1
}

const transactions_fields = ['date', 'operation', 'amount', 'currency_value']
const bot_decision_fields = ['timestamp', 'decision', 'reason']

export default {
  name: 'AuthStateApp',
  created() {
    this.unsubscribeAuth = onAuthUIStateChange((authState, authData) => {
      store.dispatch('setAuthState', authState);
      store.dispatch('setUser', authData);
      this.manageAccounts();
    })
  },
  data() {
    return {
      unsubscribeAuth: undefined,
      accounts: undefined,
      activeAccount: undefined,
      transactions: undefined,
      botDecisions: undefined,
      dataLoading: false,
      activeNavTab: NavTab.TRADE_GRAPH,
      NavTab,
      transactions_fields,
      bot_decision_fields
    }
  },
  methods: {
    manageAccounts() {
      if (this.accounts === undefined && this.currentUser !== undefined && this.currentUser.signInUserSession !== undefined) {
        let self = this;

        // load accounts and set default
        axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/accounts', this.getRequestData())
            .then(response => {
                  self.accounts = response.data.data

                  if (self.accounts !== undefined && self.accounts.length > 0) {
                    self.activeAccount = self.accounts[0];
                  }
                }
            )
      } else {
        if (this.currentUser === undefined || this.currentUser.signInUserSession === undefined) {
          this.accounts = undefined
        }
      }
    },
    getGraph() {
      this.dataLoading = true
      let url_extension = 'account-graph/'

      if (this.activeNavTab === NavTab.TRADE_GRAPH) {
        this.getTransactions(); // get transactions for the trade graph table
        url_extension = 'trade-graph/'
        this.botDecisions = undefined;
      } else {
        this.transactions = undefined; // if it's not a trade-graph tab delete them transactions
        this.getBotDecisions();
      }

      axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/' + url_extension + this.activeAccount.account_id, this.getRequestData())
          .then(response => {
                this.dataLoading = false
                const figure = JSON.parse(response.data.message);
                Plotly.newPlot('graph', figure.data, figure.layout);
              }
          )
    },
    getTransactions() {
      axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/transactions/' + this.activeAccount.account_id, this.getRequestData())
          .then(response => {
                this.transactions = response.data.data;
              }
          )
    },
    getBotDecisions() {
      axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/bot-decisions/' + this.activeAccount.account_id, this.getRequestData())
          .then(response => {
                this.botDecisions = response.data.data;
              }
          )
    },
    getRequestData() {
      const token = this.currentUser.signInUserSession.idToken.jwtToken
      return {
        headers: {
          Authorization: token
        }
      }
    },
    appSignOut: async function () {
      try {
        await Auth.signOut();
      } catch (error) {
        console.log('error signing out: ', error);
      }
    }
  },
  computed: {
    isSignedIn: function () {
      return !!(this.authState !== undefined && this.authState === 'signedin' && this.currentUser);
    },
    currentUser() {
      return this.$store.getters.currentUser
    },
    authState() {
      return this.$store.getters.authState
    }
  },
  watch: {
    activeNavTab: function () {
      this.getGraph();
    },
    activeAccount: function () {
      this.getGraph();
    }
  },
  beforeDestroy() {
    this.unsubscribeAuth();
    this.accounts = undefined;
  }
}
</script>
