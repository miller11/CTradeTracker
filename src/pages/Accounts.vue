<template>
  <div class="Accounts">
    <h3>Managed Accounts</h3>
    <b-table striped small hover :items="managedAccounts" :fields="managed_accounts_fields" sort-by="timestamp" sort-desc>
      <template #cell(remove)="data">
        <b-button variant="danger" size="sm" @click="removeAccount(data.item.account_id)">Remove</b-button>
      </template>
    </b-table>

    <form v-if="showForm" @submit="onSubmit">
        <div class="form-group row">
          <label class="col-2 col-form-label" for="fm-currency">Currency</label>
          <div class="col-5">
            <input id="fm-currency" disabled :value="accountToAdd.currency" name="fm-currency" type="text" class="form-control">
          </div>
        </div>
        <div class="form-group row">
          <label for="fm-source-currency" class="col-2 col-form-label">Source Currency</label>
          <div class="col-5">
            <input id="fm-source-currency" name="fm-source-currency" v-model="accountToAdd.source_currency"  type="text" class="form-control">
          </div>
        </div>
        <div class="form-group row">
          <label for="fm-default-buy" class="col-2 col-form-label">Default Buy</label>
          <div class="col-5">
            <input id="fm-default-buy" name="fm-default-buy" type="number" min="0" step="0.000001" v-model="accountToAdd.default_buy" class="form-control">
          </div>
        </div>
        <div class="form-group row">
          <label for="fm-short-term-periods" class="col-2 col-form-label">Short Term Periods</label>
          <div class="col-5">
            <input id="fm-short-term-periods" name="fm-short-term-periods" type="number" v-model="accountToAdd.short_term_periods" class="form-control">
          </div>
        </div>
        <div class="form-group row">
          <label for="fm-long-term-periods" class="col-2 col-form-label">Long Term Periods</label>
          <div class="col-5">
            <input id="fm-long-term-periods" name="fm-long-term-periods" value="40" type="number" v-model="accountToAdd.long_term_periods" class="form-control">
          </div>
        </div>
        <div class="form-group row">
          <div class="offset-2 col-10">
            <button name="submit" type="submit" class="btn btn-primary">Save</button>
          </div>
        </div>
      </form>

    <h3>Available Accounts</h3>
    <b-table striped small hover :items="filteredAccounts" :fields="all_accounts_fields" sort-by="timestamp" sort-desc>
      <template #cell(add)="data">
        <b-button variant="success" size="sm" @click="addAccount(data.item.id, data.item.currency)">Add</b-button>
      </template>
    </b-table>

  </div>
</template>

<script>
import axios from "axios";

const managed_accounts_fields = ['currency', 'source_currency', 'default_buy', 'long_term_periods', 'short_term_periods', 'remove']
const all_accounts_fields = ['currency', 'balance', 'trading_enabled', 'add']

export default {
  name: "Accounts",
  data() {
    return {
      managedAccounts: undefined,
      allAccounts: undefined,
      accountToAdd: undefined,
      showForm: false,
      managed_accounts_fields,
      all_accounts_fields
    }
  },
  created() {
    this.loadAccounts();
  },
  methods: {
    getRequestData() {
      const token = this.currentUser.signInUserSession.idToken.jwtToken
      return {
        headers: {
          Authorization: token
        }
      }
    },
    loadAccounts() {
      if ( this.currentUser !== undefined && this.currentUser.signInUserSession !== undefined) {
        axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/cbp-accounts', this.getRequestData())
            .then(response => {
                  this.allAccounts = response.data.data;
                }
            )

        axios.get('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/accounts', this.getRequestData())
            .then(response => {
                  this.managedAccounts = response.data.data
                }
            )
      }
    },
    addAccount(account_id, currency) {
      this.accountToAdd = {};
      this.accountToAdd.account_id = account_id;
      this.accountToAdd.currency = currency;
      this.accountToAdd.source_currency = 'USD';
      this.accountToAdd.default_buy = 0.000016;
      this.accountToAdd.long_term_periods = 40;
      this.accountToAdd.short_term_periods = 10;

      this.showForm = true
    },
    onSubmit(event) {
      event.preventDefault();

      let data = {account : this.accountToAdd}

      axios.post('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/cbp-accounts/' + this.accountToAdd.account_id, data,  this.getRequestData())
          .then(response => {
                if (response) {
                  this.loadAccounts();
                  alert('Account has been added')
                }
              }
          )

      this.showForm = false;
      this.accountToAdd = undefined;
    },
    removeAccount(account_id) {
      alert(account_id)

      axios.delete('https://n77revptog.execute-api.us-east-1.amazonaws.com/Test/cbp-accounts/' + this.accountToAdd.account_id, this.getRequestData())
          .then(response => {
                if (response) {
                  this.loadAccounts();
                  alert('Account has been removed')
                }
              }
          )
    }
  },
  computed: {
    filteredAccounts() {
      if(this.allAccounts === undefined) {
        return []
      }

      let idArray = this.managedAccounts.map(a => a.account_id)

      return this.allAccounts.filter(function isEven(account) {
        return !idArray.includes(account.id);
      });
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
