import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'characters/'
        },
    },

    actions: {
        async loadOne (ctx, characterId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: characterId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newCharacter) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newCharacter }, { root: true }
            )
        },

        async update (ctx, character) {
            return ctx.dispatch('api/update',
                { url: ctx.getters.urlPath, partialObject: character }, { root: true }
            )
        },

        async remove (ctx, characterId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: characterId }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        character: {
            person: null,
            name: null,
        },
        characters: {
            count: 0,
            next: null,
            previous: null,
            // name, person
            results: []
        }
    }),
 */
