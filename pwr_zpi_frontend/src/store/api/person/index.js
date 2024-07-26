import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'people/'
        },
    },

    actions: {
        async loadOne (ctx, personId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: personId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newPerson) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newPerson }, { root: true }
            )
        },

        async update (ctx, person) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: person }, { root: true }
            )
        },

        async remove (ctx, personId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: personId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        person: {
            name: null,
            surname: null,
            birthdate: null,
            country: null,
            details: null
        },
        people: {
            count: 0,
            next: null,
            previous: null,
            // name, surname, birthdate, country
            results: []
        }
    }),
 */
