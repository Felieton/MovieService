import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'permissions/'
        },
    },

    actions: {
        async loadOne (ctx, permissionId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: permissionId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newPermission) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newPermission }, { root: true }
            )
        },

        async update (ctx, permission) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: permission }, { root: true }
            )
        },

        async remove (ctx, permissionId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: permissionId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        permission: {
            name: null,
            codename: null
        },
        permissions: {
            count: 0,
            next: null,
            previous: null,
            // name, codename
            results: []
        }
    }),
 */
