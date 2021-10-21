<template>
  <div id="app">
    <div>
      <div>
        <b-navbar toggleable="sm" type="dark" variant="dark">
          <b-navbar-brand href="#">TradeTracker</b-navbar-brand>

          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

          <b-collapse id="nav-collapse" is-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
              <b-nav-item-dropdown v-if="authState === 'signedin' && user" right>
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



    <amplify-authenticator username-alias="email"></amplify-authenticator>
    <button type="button" @click="getGraph('bec75c28-d95a-52a9-8edf-d0947a133eda')">Call API</button>

    <div id="graph"></div>


  </div>
</template>


<script>

import {onAuthUIStateChange} from '@aws-amplify/ui-components'
import { Auth } from 'aws-amplify';
import axios from 'axios'
import Plotly from 'plotly.js-dist'

export default {
  name: 'AuthStateApp',
  created() {
    this.unsubscribeAuth = onAuthUIStateChange((authState, authData) => {
      this.authState = authState;
      this.user = authData;
    })
  },
  data() {
    return {
      user: undefined,
      authState: undefined,
      unsubscribeAuth: undefined
    }
  },
  methods: {
    getGraph(accountId) {
      const token = this.user.signInUserSession.idToken.jwtToken
      const requestData = {
        headers: {
          Authorization: token,
          "Access-Control-Allow-Origin": "*"
        }
      }

      axios.get('https://yzn99f7f90.execute-api.us-east-1.amazonaws.com/Stage/trade-graph/' + accountId, requestData)
          .then(response => {
                const figure = JSON.parse(response.data.message)
                console.log(figure)

                Plotly.newPlot('graph', figure.data, figure.layout);
              }
          )
    },
    appSignOut: async function() {
      try {
        await Auth.signOut();
        this.user = undefined;
      } catch (error) {
        console.log('error signing out: ', error);
      }
    }
  },
  beforeDestroy() {
    this.unsubscribeAuth();
  }
}


</script>
