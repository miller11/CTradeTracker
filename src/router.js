import Vue from 'vue';
import Router from 'vue-router';

import Home from './pages/Home';
import Accounts from './pages/Accounts';
import APIKey from "./pages/APIKey";


Vue.use(Router);

const router = new Router({
    mode: 'history',
    base: '/trade-tracker/',
    routes: [
        {
            path: '/',
            component: Home,
            name: 'home',
            meta: {
                title: 'Home'
            }
        },
        {
            path: '/accounts',
            component: Accounts,
            name: 'accounts',
            meta: {
                title: 'Accounts'
            }
        },
        {
            path: '/api-key',
            component: APIKey,
            name: 'apikey',
            meta: {
                title: 'API Key'
            }
        }
    ]
});

export default router;
