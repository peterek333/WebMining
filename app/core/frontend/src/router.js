import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Subscription from '@/components/Subscription'
import Visualization from '@/components/Visualization'

import store from './store'

const ENABLED_AUTH = true;

Vue.use(Router);

const router = new Router({
    mode: 'history', // uris without hashes #, see https://router.vuejs.org/guide/essentials/history-mode.html#html5-history-mode
    routes: [
        { path: '/login', component: Login },
        {
            path: '/subscription',
            alias: '/',
            component: Subscription,
            meta: {
                requiresAuth: ENABLED_AUTH
            }
        },
        {
            path: '/visualization',
            component: Visualization,
            meta: {
                requiresAuth: ENABLED_AUTH
            }
        },

        // otherwise redirect to home
        { path: '*', redirect: '/' }
    ]
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // this route requires auth, check if logged in
        // if not, redirect to login page.
        if (!store.getters.isLoggedIn) {
            next({
                path: '/login'
            })
        } else {
            next();
        }
    } else {
        next(); // make sure to always call next()!
    }
});

export default router;