import apiCfg from '../config'


export default {
    namespaced: true,
    getters: {
        urlPath() {
            return apiCfg.baseUrl + 'users/'
        },
    },

    actions: {
        async loadOne (ctx, userId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: userId }, { root: true }
            )
        },
        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },
        async create (ctx, newUser) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newUser }, { root: true }
            )
        },
        async update (ctx, user) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: user }, { root: true }
            )
        },
        async remove (ctx, userId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: userId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        user: {
            username: null,
            email: null,
            groups: [],
            user_permissions: [],
            is_active: null,
            is_superuser: null,
            is_staff: null,
            is_removed: null,
            last_login: null, // "2021-10-14T16:41:33.124072Z"
            date_joined: null, // "2021-08-23T16:14:29Z"
        },
        users: {
            count: 0,
            next: null,
            previous: null,
            // url, username, email, groups, is_active
            results: []
        }
    }),
 */
