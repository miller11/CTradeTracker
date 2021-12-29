import Vue from 'vue';
import Router from 'vue-router';

import Home from './pages/Home';
import Accounts from './pages/Accounts';


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
        }
    ]
});

export default router;
