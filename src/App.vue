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
              <b-nav-item-dropdown text="Select Account"  right>
                <b-dropdown-item v-for="(account) in accounts" :key="account.account_id" @click="activeAccount = account;">{{ account.name }}</b-dropdown-item>
              </b-nav-item-dropdown>

              <b-nav-item href="#" v-if="activeAccount !== undefined" disabled>{{ activeAccount.name }}</b-nav-item>


              <b-nav-item-dropdown  right>
                <!-- Using 'button-content' slot -->
                <template #button-content>
                  <em>{{ user.attributes.email }}</em>
                </template>
                <b-dropdown-item @click="appSignOut()">Sign Out</b-dropdown-item>
              </b-nav-item-dropdown>
            </b-navbar-nav>
          </b-collapse>
        </b-navbar>
      </div>
    </div>


    <div v-if="activeAccount !== undefined">
      <b-card :title="activeAccount.name" no-body>
        <b-card-header header-tag="nav">
          <b-nav card-header tabs>
            <b-nav-item active>Transactions</b-nav-item>
            <b-nav-item>Gain/Loss</b-nav-item>
          </b-nav>
        </b-card-header>

        <b-card-body class="text-center">
          <b-card-text>
            With supporting text below as a natural lead-in to additional content.
          </b-card-text>

          <b-button variant="primary">Go somewhere</b-button>
        </b-card-body>
      </b-card>
    </div>


    <amplify-authenticator username-alias="email"></amplify-authenticator>




<!--    <button type="button" @click="getGraph('bec75c28-d95a-52a9-8edf-d0947a133eda')">Call API</button>-->

    <div id="graph"></div>


  </div>
</template>


<script>

import {onAuthUIStateChange} from '@aws-amplify/ui-components'
import {Auth} from 'aws-amplify';
import axios from 'axios'
import Plotly from 'plotly.js-dist'

export default {
  name: 'AuthStateApp',
  created() {
    this.unsubscribeAuth = onAuthUIStateChange((authState, authData) => {
      this.authState = authState;
      this.user = authData;
      this.loadAccounts();
    })
  },
  data() {
    return {
      user: undefined,
      authState: undefined,
      unsubscribeAuth: undefined,
      accounts: undefined,
      activeAccount: undefined
    }
  },
  methods: {
    loadAccounts() {
      if(this.user !== undefined && this.user.signInUserSession !== undefined) {
        let self = this;
        const token = this.user.signInUserSession.idToken.jwtToken
        const requestData = {
          headers: {
            Authorization: token
          }
        }

        axios.get('https://2q0agbdysd.execute-api.us-east-1.amazonaws.com/Test/accounts', requestData)
            .then(response => {
                  self.accounts = response.data.data
                }
            )
      }
    },
    getGraph(accountId) {
      const token = this.user.signInUserSession.idToken.jwtToken
      const requestData = {
        headers: {
          Authorization: token
        }
      }

      axios.get('https://2q0agbdysd.execute-api.us-east-1.amazonaws.com/Test/trade-graph/' + accountId, requestData)
          .then(response => {
                const figure = JSON.parse(response.data.message)
                console.log(figure)

                Plotly.newPlot('graph', figure.data, figure.layout);
              }
          )
    },
    appSignOut: async function () {
      try {
        await Auth.signOut();
        this.user = undefined;
      } catch (error) {
        console.log('error signing out: ', error);
      }
    }
  },
  computed: {
    isSignedIn: function() {
      return this.authState === 'signedin' && this.user
    }
  },
  beforeDestroy() {
    this.unsubscribeAuth();
  }
}


</script>
