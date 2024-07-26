import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'castRoles/'
        },
    },

    actions: {
        async loadOne (ctx, castRoleId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: castRoleId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newCastRole) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newCastRole }, { root: true }
            )
        },

        async update (ctx, castRole) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: castRole }, { root: true }
            )
        },

        async remove (ctx, castRoleId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: castRoleId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        castRole: {
            title: null,
            episode: null,
            person: null,
            roles: null
        },
        castRoles: {
            count: 0,
            next: null,
            previous: null,
            // title, episode, person, roles
            results: []
        }
    }),
 */
