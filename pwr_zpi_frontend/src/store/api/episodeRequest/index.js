import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'episodeRequests/'
        },
    },

    actions: {
        async loadOne (ctx, episodeRequestId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: episodeRequestId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newEpisodeRequest) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newEpisodeRequest }, { root: true }
            )
        },

        async update (ctx, episodeRequest) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: episodeRequest }, { root: true }
            )
        },

        async remove (ctx, episodeRequestId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: episodeRequestId }, { root: true }
            )
        },

        async accept (ctx, data) {
            return ctx.dispatch('api/accept',
                { url: ctx.getters.urlPath, data }, { root: true }
            )
        },

        async reject (ctx, data) {
            return ctx.dispatch('api/reject',
                { url: ctx.getters.urlPath, data }, { root: true }
            )
        },
    },
}

/*
state: () => ({
        titleRequest: {
            action: null,
            user: null,
            status: null,
            header: null,
            description: null,
            pending: null,
            episodeSubmission: null,
            currentEpisode: null
        },
        episodeRequests: {
            count: 0,
            next: null,
            previous: null,
            // action, user, status, header, description, pending, currentEpisode, episodeSubmission
            results: []
        }
    }),
 */
