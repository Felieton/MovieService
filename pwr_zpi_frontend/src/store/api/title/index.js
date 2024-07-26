import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'titles/'
        },
    },

    actions: {
        async loadOne (ctx, titleId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: titleId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newTitle) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newTitle }, { root: true }
            )
        },

        async update (ctx, title) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: title }, { root: true }
            )
        },

        async remove (ctx, titleId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: titleId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        title: {
            title: null,
            year: null,
            plot: null,
            created: null,
            type: null,
            duration: null,
            released: null,
            seasonCount: null,
            characters: null,
            countries: null,
            genres: null,
            languages: null,
            rating: null
        },
        titles: {
            count: 0,
            next: null,
            previous: null,
            // title, year, created, type, duration, released ,seasonsCount, genres, rating
            results: []
        }
    }),
 */
