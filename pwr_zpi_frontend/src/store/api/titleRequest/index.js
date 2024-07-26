import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'titleRequests/'
        },
    },

    actions: {
        async loadOne (ctx, titleRequestId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: titleRequestId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newTitleRequest) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newTitleRequest }, { root: true }
            )
        },

        async update (ctx, titleRequest) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: titleRequest }, { root: true }
            )
        },

        async remove (ctx, titleRequestId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: titleRequestId }, { root: true }
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
            titleSubmission: null,
            currentTitle: null
        },
        titleRequests: {
            count: 0,
            next: null,
            previous: null,
            // action, user, status, header, description, pending, currentTitle, titleSubmission
            results: []
        }
    }),
 */
