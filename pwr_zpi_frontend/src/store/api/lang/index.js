import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'languages/'
        },
    },

    actions: {
        async loadOne (ctx, langId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: langId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newLang) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newLang }, { root: true }
            )
        },

        async update (ctx, lang) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: lang }, { root: true }
            )
        },

        async remove (ctx, langId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: langId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        lang: {
            name: null,
        },
        langs: {
            count: 0,
            next: null,
            previous: null,
            // name
            results: []
        }
    }),
*/
