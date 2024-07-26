import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'titleSubmissions/'
        },
    },

    actions: {
        async loadOne (ctx, titleSubmissionId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: titleSubmissionId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newTitleSubmission) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newTitleSubmission }, { root: true }
            )
        },

        async update (ctx, titleSubmission) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: titleSubmission }, { root: true }
            )
        },

        async remove (ctx, titleSubmissionId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: titleSubmissionId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        titleSubmission: {
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
        titleSubmissions: {
            count: 0,
            next: null,
            previous: null,
            // title, year, created, type, duration, released ,seasonsCount, genres, rating
            results: []
        }
    }),
 */
