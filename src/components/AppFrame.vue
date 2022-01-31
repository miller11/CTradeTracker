<template>
  <div class="AppFrame">
    <div>
      <div>
        <b-navbar toggleable="sm" type="dark" variant="dark">
          <router-link :to="{name: 'home'}">
            <b-navbar-brand>TradeTracker</b-navbar-brand>
          </router-link>

          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

          <b-collapse id="nav-collapse" v-if="isSignedIn" is-nav>
            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
              <b-nav-item @click="$router.push({name: 'trades'})">Trades</b-nav-item>

              <b-nav-item-dropdown right>
                <!-- Using 'button-content' slot -->
                <template #button-content>
                  <em>{{ currentUser.attributes.email }}</em>
                </template>
                <b-dropdown-item @click="$router.push({name: 'accounts'})">Manage Accounts</b-dropdown-item>
                <b-dropdown-item @click="$router.push({name: 'apikey'})">Manage API Key</b-dropdown-item>
                <b-dropdown-item @click="appSignOut()">Sign Out</b-dropdown-item>
              </b-nav-item-dropdown>
            </b-navbar-nav>
          </b-collapse>
        </b-navbar>
      </div>
    </div>


    <div class="container mt-4">
      <!-- Content here -->
      <slot></slot>
    </div>

  </div>

</template>

<script>
import {onAuthUIStateChange} from '@aws-amplify/ui-components'
import {Auth} from 'aws-amplify';
import {store} from '@/store/store';


export default {
  name: "AppFrame",
  data() {
    return {
      unsubscribeAuth: undefined
    }
  },
  created() {
    this.unsubscribeAuth = onAuthUIStateChange((authState, authData) => {
      store.dispatch('setAuthState', authState);
      store.dispatch('setUser', authData);
    })
  },
  methods: {
    appSignOut: async function () {
      try {
        await Auth.signOut().then(response => {
              console.log(response);
              this.$router.push({name: 'home'});
            }
        )
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
  beforeDestroy() {
    this.unsubscribeAuth();
  }
}
</script>

<style scoped>

</style>
