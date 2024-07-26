import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'castMembers/'
        },
    },

    actions: {
        async loadOne (ctx, castMemberId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: castMemberId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newCastMember) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newCastMember }, { root: true }
            )
        },

        async update (ctx, castMember) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: castMember }, { root: true }
            )
        },

        async remove (ctx, castMemberId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: castMemberId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        castMember: {
            name: null,
        },
        castMembers: {
            count: 0,
            next: null,
            previous: null,
            // name
            results: []
        }
    }),
 */
