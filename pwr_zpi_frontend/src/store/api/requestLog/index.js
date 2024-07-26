import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'requestLogs/'
        },
    },

    actions: {
        async loadOne (ctx, requestLogId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: requestLogId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newRequestLog) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newRequestLog }, { root: true }
            )
        },

        async update (ctx, requestLog) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: requestLog }, { root: true }
            )
        },

        async remove (ctx, requestLogId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: requestLogId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        requestLog: {
            titleRequest: null,
            episodeRequest: null,
            personRequest: null,
            moderator: null,
            details: null,
            created: null
        },
        requestLogs: {
            count: 0,
            next: null,
            previous: null,
            // titleRequest, episodeRequest, personRequest, moderator, details, created
            results: []
        }
    }),
 */
