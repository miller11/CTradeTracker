<template>
  <div class="Home mb-5">
    <div class="row">
      <div class="col-sm-2">
        <b-form-select v-model="activeAccountId" :options="accounts" value-field="account_id" text-field="currency"></b-form-select>
      </div>
      <div class="offset-sm-6 col-sm-4">
        <h4 class="mt-1" v-if="activeCbpAccount !== undefined">Account Balance(USD): {{ activeCbpAccount.usd_balance | currency }}</h4>
      </div>
    </div>


      <div v-if="activeAccountId !== undefined">
        <ul class="nav nav-tabs mt-3">
          <li class="nav-item">
            <a class="nav-link" :class="{ active: activeNavTab === NavTab.TRADE_GRAPH }"
               @click="activeNavTab = NavTab.TRADE_GRAPH">Trades</a>
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
            <b-table striped hover :items="transactions" :fields="transactions_fields" sort-by="timestamp" sort-desc></b-table>
          </div>
        </div>

        <div class="row" v-if="botDecisions !== undefined">
          <div class="col-12">
            <h3>Bot Decisions</h3>
            <b-table striped hover :items="botDecisions" :fields="bot_decision_fields" sort-by="timestamp" sort-desc></b-table>
          </div>
        </div>
      </div>
  </div>
</template>


<script>
import axios from 'axios'

import Plotly from 'plotly.js-dist'

const NavTab = {
  TRADE_GRAPH: 0,
  GAIN_LOSS: 1
}

const transactions_fields = ['date', 'operation', 'amount', 'price']
const bot_decision_fields = ['timestamp', 'decision', 'reason']

export default {
  name: 'Home',
  data() {
    return {
      unsubscribeAuth: undefined,
      accounts: undefined,
      cbpAccounts: undefined,
      activeAccountId: undefined,
      activeCbpAccount: undefined,
      transactions: undefined,
      botDecisions: undefined,
      dataLoading: false,
      activeNavTab: NavTab.TRADE_GRAPH,
      NavTab,
      transactions_fields,
      bot_decision_fields
    }
  },
  mounted() {
    this.manageAccounts();
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
                    self.activeAccountId = self.accounts[0].account_id;
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

      axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/' + url_extension + this.activeAccountId, this.getRequestData())
          .then(response => {
                this.dataLoading = false
                const figure = JSON.parse(response.data.message);
                Plotly.newPlot('graph', figure.data, figure.layout);
              }
          )
    },
    getTransactions() {
      axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/transactions/' + this.activeAccountId, this.getRequestData())
          .then(response => {
                this.transactions = response.data.data;
              }
          )
    },
    getBotDecisions() {
      axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/bot-decisions/' + this.activeAccountId, this.getRequestData())
          .then(response => {
                this.botDecisions = response.data.data;
              }
          )
    },
    getCBPAccount() {
      axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/cbp-account/' + this.activeAccountId, this.getRequestData())
          .then(response => {
                this.activeCbpAccount = response.data.data;
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
    }
  },
  computed: {
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
    activeAccountId: function () {
      this.getGraph();
      this.getCBPAccount();
    }
  },
  beforeDestroy() {
    this.accounts = undefined;
  }
}
</script>
