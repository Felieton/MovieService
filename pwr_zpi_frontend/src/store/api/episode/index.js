import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'episodes/'
        },
    },

    actions: {
        async loadOne (ctx, episodeId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: episodeId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newEpisode) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newEpisode }, { root: true }
            )
        },

        async update (ctx, episode) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: episode }, { root: true }
            )
        },

        async remove (ctx, episodeId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: episodeId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        episode: {
            name: null,
            title: null,
            plot: null,
            created: null,
            season: null,
            duration: null,
            released: null,
            number: null,
            characters: null,
            rating: null
        },
        episodes: {
            count: 0,
            next: null,
            previous: null,
            // name, title, created, duration, released ,season, number, rating
            results: []
        }
    }),
 */
