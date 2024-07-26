import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'countries/'
        },
    },

    actions: {
        async loadOne (ctx, countryId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: countryId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newCountry) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newCountry }, { root: true }
            )
        },

        async update (ctx, country) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: country }, { root: true }
            )
        },

        async remove (ctx, countryId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: countryId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        country: {
            name: null,
        },
        countries: {
            count: 0,
            next: null,
            previous: null,
            // name
            results: []
        }
    }),
 */
