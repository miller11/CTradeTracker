import Vue from 'vue';
import Router from 'vue-router';

import Home from './pages/Home';
import Trades from './pages/Trades';
import Accounts from './pages/Accounts';
import APIKey from "./pages/APIKey";
import Auth from "./pages/Auth"
import {store} from '@/store/store'

Vue.use(Router);

const router = new Router({
    mode: 'history',
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
            path: '/trades',
            component: Trades,
            name: 'trades',
            meta: {
                title: 'Trades',
                requiresAuth: true
            }
        },
        {
            path: '/accounts',
            component: Accounts,
            name: 'accounts',
            meta: {
                title: 'Accounts',
                requiresAuth: true
            }
        },
        {
            path: '/api-key',
            component: APIKey,
            name: 'apikey',
            meta: {
                title: 'API Key',
                requiresAuth: true
            }
        },
        {
            path: '/auth',
            component: Auth,
            name: 'auth',
            meta: {
                title: 'Auth'
            }
        }
    ]
});

router.beforeResolve((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if(store.getters.authState !== undefined && store.getters.authState === 'signedin' && store.getters.currentUser) {
            next()
        } else {
            next({
                path: '/auth'
            });
        }
    }

    next()
})

export default router;
