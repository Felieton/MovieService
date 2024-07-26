import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'actionLogs/'
        },
    },

    actions: {
        async loadOne (ctx, actionLogId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: actionLogId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newActionLog) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newActionLog }, { root: true }
            )
        },

        async update (ctx, actionLog) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: actionLog }, { root: true }
            )
        },

        async remove (ctx, actionLogId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: actionLogId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        actionLog: {
            ipAddress: null,
            user: null,
            moderator: null,
            details: null,
            created: null
        },
        actionLogs: {
            count: 0,
            next: null,
            previous: null,
            // moderator, created, details, user, ipAddress
            results: []
        }
    }),
 */
