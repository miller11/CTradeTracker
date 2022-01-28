<template>
  <div class="APIKey">
    <h3>Add API Key</h3>

    <hr/>

    <div v-if="keySaved" class="alert alert-primary" role="alert">
      API Key Currently on file
    </div>

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
import ApiClient from '../../jsUtil/APIClient';

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
  mounted() {
    this.getKeyStatus();
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();

      let data = {accessKey : this.accessKey,
                  passphrase : this.passphrase,
                  secret : this.secret}

      new ApiClient().setAPIKey(data)
          .then(response => {
                if (response) {
                  this.getKeyStatus()
                  alert(response.data.data)
                }
              }
          )
    },
    getKeyStatus() {
      new ApiClient().getAPIKeyStatus()
          .then(response => {
            this.keySaved  = response.data.data.keySaved;
          })
    }
  }
}

</script>

<style scoped>

</style>
