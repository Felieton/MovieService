import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import axios from 'axios';
import VueAuthenticate from 'vue-authenticate'

import providers from '../providers'
import api from './api'
import storeCfg from "./config";
import {GROUP_MOD, GROUP_ADMIN, GROUPS_ACCESS} from "./group_types";

Vue.use(Vuex)

// mount 'axios', '$http' properties to Vue instance
Object.defineProperties(Vue.prototype, {
    axios: {
        value: axios
    },
    $http: {
        value: axios
    }
})

const authCfg = {
    login: {
        url: 'o/login/'
    },
    logout: {
        url: 'o/logout/',
        tokenKey: 'token',
    },
    register: {
        url: 'o/registration/'
    },
    refreshToken: {
        storageKey: 'refresh_token',
        responseKey: 'refresh_token',
        url: 'o/token/refresh/',
        accessTokenPath: 'access',
    }
}


const vueAuth = VueAuthenticate.factory(Vue.prototype.$http, {
    baseUrl: storeCfg.baseUrl,
    loginUrl: authCfg.login.url,
    logoutUrl: authCfg.logout.url,
    registerUrl: authCfg.register.url,
    providers,
    bindRequestInterceptor: () => {},
    bindResponseInterceptor: () => {},
})

axios.interceptors.request.use( (config) => {
    const token = vueAuth.getToken()
    if (token !== null) {
        config.headers['Authorization'] = ['Bearer', token].join(' ')
    }

    return config
})

export default new Vuex.Store({
    plugins: [createPersistedState({
        storage: window.localStorage,
    })],
    state: {
        isAuthenticated: vueAuth.isAuthenticated(),
        loggedUser: {}
    },

    getters: {
        isAuthenticated (state) {
            return state.isAuthenticated
        },
        loggedUser (state) {
            return state.loggedUser;
        },
        loggedUserHasGroup: (state, getters) => (groupName) => {
            if (typeof groupName !== 'string') return false
            return GROUPS_ACCESS[getters.loggedUser?.group?.name] >= GROUPS_ACCESS[groupName]
        },
        // alias for loggedUserIsMod but more clear
        loggedUserIsStaff: (state, getters) => {
            return getters.loggedUserIsMod
        },
        loggedUserIsMod: (state, getters) => {
            return getters.loggedUserHasGroup(GROUP_MOD)
        },
        loggedUserIsAdmin: (state, getters) => {
            return getters.loggedUserHasGroup(GROUP_ADMIN)
        },
    },

    mutations: {
        isAuthenticated (state, payload) {
            state.isAuthenticated = payload.isAuthenticated
        },
        loggedUser (state, payload) {
            state.loggedUser = payload.loggedUser
        }
    },

    actions: {
        setRefreshToken (ctx, data={}) {
            if (typeof data !== 'object' || data === null) return

            if (authCfg.refreshToken.responseKey in data)
                localStorage.setItem(authCfg.refreshToken.storageKey, data[authCfg.refreshToken.responseKey])
            else
                localStorage.setItem(authCfg.refreshToken.storageKey, '')
        },

        async refreshToken() {
            const requestData = {
                refresh: localStorage.getItem(authCfg.refreshToken.storageKey)
            }
            await axios.post(`${storeCfg.baseUrl}${authCfg.refreshToken.url}`, requestData).then( (res) => {
                vueAuth.setToken(res, authCfg.refreshToken.accessTokenPath)
            })
        },

        async initLoggedUserData(ctx, payload) {
            const userResponse = await ctx.dispatch('api/user/loadOne', payload.userId)
            const groups = userResponse.data.groups
            // Since we only need to know group with the highest access level
            const best_group = groups && groups.length ? groups.reduce( (prev, current) => (
                GROUPS_ACCESS[prev.name] > GROUPS_ACCESS[current.name]) ? prev : current
            ) : ''
            ctx.commit('loggedUser', {
                loggedUser:  {
                    id: userResponse.data.id,
                    username: userResponse.data.username,
                    photo: userResponse.data.photo,
                    group: best_group,
                }
            })
        },

        async login (ctx, payload) {
            await ctx.dispatch('setRefreshToken')
            let res = await vueAuth.login(payload.user, {})
            ctx.dispatch('initLoggedUserData', {
                userId: res.data.user.pk
            })
            ctx.dispatch('setRefreshToken', res.data)
            ctx.commit('isAuthenticated', {
                isAuthenticated: vueAuth.isAuthenticated()
            })
        },

        async logout (ctx, requestOptions) {
            requestOptions = requestOptions ? requestOptions : {}
            requestOptions.data = {}
            requestOptions.data[authCfg.logout.tokenKey] = vueAuth.getToken()
            await vueAuth.logout(requestOptions)
            ctx.dispatch('setRefreshToken')
            ctx.commit('isAuthenticated', {
                isAuthenticated: vueAuth.isAuthenticated()
            })
            ctx.commit('loggedUser', {
                loggedUser: {}
            })
        },

        async register (ctx, payload) {
            const res = await vueAuth.register(payload.user, {})
            ctx.commit('isAuthenticated', {
                isAuthenticated: vueAuth.isAuthenticated()
            })
            return res;
        },

        async authWithProvider (ctx, provider) {
            await ctx.dispatch('setRefreshToken')
            const res = await vueAuth.authenticate(provider, {})
            ctx.dispatch('initLoggedUserData', {
                userId: res.data.user.pk
            })
            ctx.dispatch('setRefreshToken', res.data)
            ctx.commit('isAuthenticated', {
                isAuthenticated: vueAuth.isAuthenticated()
            })
        },
    },

    modules: {
        api,
    },
})
