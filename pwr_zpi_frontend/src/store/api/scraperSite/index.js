import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'scraperSites/'
        },
    },

    actions: {
        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newScraperSite) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newScraperSite }, { root: true }
            )
        },

        async update (ctx, scraperSite) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: scraperSite }, { root: true }
            )
        },

        async remove (ctx, scraperSiteId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: scraperSiteId }, { root: true }
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
