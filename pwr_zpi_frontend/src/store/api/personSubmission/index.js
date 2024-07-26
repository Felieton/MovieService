import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'personSubmissions/'
        },
    },

    actions: {
        async loadOne (ctx, personSubmissionId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: personSubmissionId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newPersonSubmission) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newPersonSubmission }, { root: true }
            )
        },

        async update (ctx, personSubmission) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: personSubmission }, { root: true }
            )
        },

        async remove (ctx, personSubmissionId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: personSubmissionId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        personSubmission: {
            name: null,
            surname: null,
            birthdate: null,
            country: null,
            details: null
        },
        personSubmissions: {
            count: 0,
            next: null,
            previous: null,
            // name, surname, birthdate, country
            results: []
        }
    }),
 */
