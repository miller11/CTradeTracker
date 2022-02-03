<template>
  <div class="Home mb-5">
    <div class="row">
      <div class="col-sm-2">
        <b-form-select v-model="activeAccountId" :options="accounts" value-field="account_id"
                       text-field="currency"></b-form-select>
        <b-spinner v-if="accountsLoading" variant="success" label="Loading"></b-spinner>
      </div>
      <div class="offset-sm-6 col-sm-4">
        <h4 class="mt-1" v-if="activeCbpAccount !== undefined">Account Balance(USD):
          {{ activeCbpAccount.usd_balance | currency }}</h4>
        <h5 class="mt-1 text-muted" v-if="activeCbpAccount !== undefined">Current Price(USD):
          {{ activeCbpAccount.current_price | currency }}</h5>
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
          <div class="col-sm-3 offset-sm-9 mt-2">
            Days
            <b-button-group size="sm">
              <b-button variant="primary" :pressed="daysBack === 7" @click="daysBack = 7">7</b-button>
              <b-button variant="primary" :pressed="daysBack === 14" @click="daysBack = 14">14</b-button>
              <b-button variant="primary" :pressed="daysBack === 30" @click="daysBack = 30">30</b-button>
              <b-button variant="primary" :pressed="daysBack === 90" @click="daysBack = 90">90</b-button>
            </b-button-group>
          </div>

          <div v-if="dataLoading" class="row">
            <b-spinner variant="success" label="Loading"></b-spinner>
          </div>
          <div id="graph"></div>
        </div>
      </div>

      <div class="row" v-if="transactions !== undefined">
        <div class="col-12">
          <h3>Transactions</h3>
          <b-table striped hover :items="transactions" :fields="transactions_fields" sort-by="timestamp" sort-desc>
            <template #cell(amount_usd)="data">
              {{ (data.item.amount * data.item.price) | currency }}
            </template>
          </b-table>
        </div>
      </div>

      <div class="row" v-if="botDecisions !== undefined">
        <div class="col-12">
          <h3>Bot Decisions</h3>
          <b-table striped hover :items="botDecisions" :fields="bot_decision_fields" sort-by="timestamp"
                   sort-desc></b-table>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import ApiClient from '../../jsUtil/APIClient';

import Plotly from 'plotly.js-dist'
import {store} from "@/store/store";

const NavTab = {
  TRADE_GRAPH: 0,
  GAIN_LOSS: 1
}

const transactions_fields = ['date', 'operation', 'amount', 'amount_usd', 'price']
const bot_decision_fields = ['timestamp', 'decision', 'reason']

export default {
  name: 'Home',
  data() {
    return {
      unsubscribeAuth: undefined,
      daysBack: 14,
      cbpAccounts: undefined,
      activeAccountId: undefined,
      activeCbpAccount: undefined,
      transactions: undefined,
      botDecisions: undefined,
      dataLoading: false,
      accountsLoading: false,
      activeNavTab: NavTab.TRADE_GRAPH,
      NavTab,
      transactions_fields,
      bot_decision_fields
    }
  },
  created() {
    this.manageAccounts();
  },
  mounted() {
    this.manageAccounts();
  },
  methods: {
    manageAccounts() {
      let loadedAccounts = undefined;
      this.accountsLoading = true;

      if (this.accounts === undefined && this.currentUser !== undefined && this.currentUser.signInUserSession !== undefined) {
        let self = this;

        // load accounts and set default
        new ApiClient().getAccounts()
            .then(response => {
              loadedAccounts = response.data.data
              store.dispatch('setManagedAccounts', loadedAccounts);

                  if (loadedAccounts !== undefined && loadedAccounts.length > 0) {
                    self.activeAccountId = loadedAccounts[0].account_id;
                  }

                  self.accountsLoading = false;
                }
            )
      } else {
        if (this.currentUser === undefined || this.currentUser.signInUserSession === undefined) {
          store.dispatch('setManagedAccounts', undefined);
          this.accountsLoading = false;
        }
      }
    },
    getGraph() {
      this.dataLoading = true
      let axiosCall = new ApiClient().getAccountGraph(this.activeAccountId, this.daysBack);

      if (this.activeNavTab === NavTab.TRADE_GRAPH) {
        this.getTransactions(); // get transactions for the trade graph table
        axiosCall = new ApiClient().getTradeGraph(this.activeAccountId, this.daysBack);
        this.botDecisions = undefined;
      } else {
        this.transactions = undefined; // if it's not a trade-graph tab delete them transactions
        this.getBotDecisions();
      }

      axiosCall
          .then(response => {
                this.dataLoading = false
                const figure = JSON.parse(response.data.message);
                Plotly.newPlot('graph', figure.data, figure.layout);
              }
          )
    },
    getTransactions() {
      new ApiClient().getTransactions(this.activeAccountId, this.daysBack)
          .then(response => {
                this.transactions = response.data.data;
              }
          )
    },
    getBotDecisions() {
      new ApiClient().getBotDecisions(this.activeAccountId, this.daysBack)
          .then(response => {
                this.botDecisions = response.data.data;
              }
          )
    },
    getCBPAccount() {
      new ApiClient().getCBPAccount(this.activeAccountId)
          .then(response => {
                this.activeCbpAccount = response.data.data;
              }
          )
    }
  },
  computed: {
    currentUser() {
      return this.$store.getters.currentUser
    },
    authState() {
      return this.$store.getters.authState
    },
    accounts() {
      return this.$store.getters.managedAccounts
    }
  },
  watch: {
    activeNavTab: function () {
      this.getGraph();
    },
    daysBack: function () {
      this.getGraph();
    },
    activeAccountId: function () {
      this.getGraph();
      this.getCBPAccount();
    }
  }
}
</script>
