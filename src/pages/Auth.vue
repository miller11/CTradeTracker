<template>
  <div>
    <amplify-auth-container>
      <amplify-authenticator username-alias="email"></amplify-authenticator>
    </amplify-auth-container>
  </div>
</template>

<script>
import {onAuthUIStateChange} from "@aws-amplify/ui-components";
import {store} from "@/store/store";

export default {
  name: "Auth",
  data() {
    return {
      unsubscribeAuth: undefined
    }
  },
  created() {
    this.unsubscribeAuth = onAuthUIStateChange((authState, authData) => {
      store.dispatch('setAuthState', authState);
      store.dispatch('setUser', authData);
      if (this.isSignedIn) {
        this.$router.push({name: 'trades'})
      }
    })
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
  }
}
</script>

<style scoped>

</style>
