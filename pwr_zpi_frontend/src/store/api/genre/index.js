import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'genres/'
        },
    },

    actions: {
        async loadOne (ctx, genreId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: genreId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newGenre) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newGenre }, { root: true }
            )
        },

        async update (ctx, genre) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: genre }, { root: true }
            )
        },

        async remove (ctx, genreId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: genreId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        genre: {
            name: null,
        },
        genres: {
            count: 0,
            next: null,
            previous: null,
            // name
            results: []
        }
    }),
 */
