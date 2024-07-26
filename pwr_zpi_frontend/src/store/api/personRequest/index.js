import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'personRequests/'
        },
    },

    actions: {
        async loadOne (ctx, personRequestId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: personRequestId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newPersonRequest) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newPersonRequest }, { root: true }
            )
        },

        async update (ctx, personRequest) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: personRequest }, { root: true }
            )
        },

        async remove (ctx, personRequestId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: personRequestId }, { root: true }
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
        personRequest: {
            action: null,
            user: null,
            status: null,
            header: null,
            created: null,
            currentPerson: null,
            personSubmission: null
        },
        personRequests: {
            count: 0,
            next: null,
            previous: null,
            // action, user, status, header, created, currentPerson, personSubmission
            results: []
        }
    }),
 */
