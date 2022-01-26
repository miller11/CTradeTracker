<template>
  <div class="APIKey">
    <h3>Add API Key</h3>
    <h4 v-if="keySaved" class="text-primary">Key Currently on file</h4>

    <hr/>



    <form @submit="onSubmit">

      <div class="form-group row">
        <label for="fm-accessKey" class="col-2 col-form-label">Access Key</label>
        <div class="col-5">
          <input id="fm-accessKey" name="fm-source-currency" v-model="accessKey"  type="text" class="form-control">
        </div>
      </div>
      <div class="form-group row">
        <label for="fm-passphrase" class="col-2 col-form-label">Passphrase</label>
        <div class="col-5">
          <input id="fm-passphrase" name="fm-source-currency" v-model="passphrase"  type="password" class="form-control">
        </div>
      </div>
      <div class="form-group row">
        <label for="fm-secret" class="col-2 col-form-label">Secret</label>
        <div class="col-5">
          <input id="fm-secret" name="fm-source-currency" v-model="secret"  type="password" class="form-control">
        </div>
      </div>
      <div class="form-group row">
        <div class="offset-2 col-10">
          <button name="submit" type="submit" class="btn btn-primary">Save</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "APIKey",
  data() {
    return {
      keySaved: false,
      accessKey: undefined,
      passphrase: undefined,
      secret: undefined
    }
  },
  created() {
    this.getKeyStatus();
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();

      let data = {accessKey : this.accessKey,
                  passphrase : this.passphrase,
                  secret : this.secret}

      axios.post('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/api-key', data,  this.getRequestData())
          .then(response => {
                if (response) {
                  this.loadAccounts();

                  alert(response.data.data)
                }
              }
          )
    },
    getKeyStatus() {
      axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/cbp-accounts', this.getRequestData())
          .then(response => {
                this.keySaved = response.data.data.keySaved;
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
  }
}
</script>

<style scoped>

</style>
