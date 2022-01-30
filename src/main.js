import Vue from 'vue'
import App from './App.vue'
import Vuex from 'vuex'
import router from './router';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import "@aws-amplify/ui-vue";
import Amplify from "aws-amplify";
import awsconfig from "./aws-exports";
import {store} from "./store/store";
import Vue2Filters from 'vue2-filters'
import Notifications from 'vue-notification'


Amplify.configure(awsconfig);

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

// Add Vuex storage
Vue.use(Vuex)

Vue.use(Vue2Filters)

Vue.use(Notifications)

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
