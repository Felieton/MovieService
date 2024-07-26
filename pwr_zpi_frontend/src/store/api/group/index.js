import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'groups/'
        },
    },

    actions: {
        async loadOne (ctx, groupId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: groupId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newGroup) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newGroup }, { root: true }
            )
        },

        async update (ctx, group) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: group }, { root: true }
            )
        },

        async remove (ctx, groupId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: groupId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        group: {
            name: null,
            permissions: null
        },
        groups: {
            count: 0,
            next: null,
            previous: null,
            // name, permissions
            results: []
        }
    }),
 */
