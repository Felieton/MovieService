import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'episodeSubmissions/'
        },
    },

    actions: {
        async loadOne (ctx, episodeSubmissionId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: episodeSubmissionId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newEpisodeSubmission) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newEpisodeSubmission }, { root: true }
            )
        },

        async update (ctx, episodeSubmission) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: episodeSubmission }, { root: true }
            )
        },

        async remove (ctx, episodeSubmissionId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: episodeSubmissionId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        episodeSubmission: {
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
        episodeSubmissions: {
            count: 0,
            next: null,
            previous: null,
            // name, title, created, duration, released ,season, number, rating
            results: []
        }
    }),
 */
