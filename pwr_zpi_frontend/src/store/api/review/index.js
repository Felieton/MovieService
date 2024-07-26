import apiCfg from '../config'

export default {
    namespaced: true,
    getters: {
        urlPath(){
            return apiCfg.baseUrl + 'reviews/'
        },
    },

    actions: {
        async loadOne (ctx, reviewId) {
            return ctx.dispatch('api/loadOne',
                { url: ctx.getters.urlPath, id: reviewId }, { root: true }
            )
        },

        async loadMany (ctx, params) {
            return ctx.dispatch('api/loadMany',
                { url: ctx.getters.urlPath, params }, { root: true }
            )
        },

        async create (ctx, newReview) {
            return ctx.dispatch('api/create',
                { url: ctx.getters.urlPath, newObject: newReview }, { root: true }
            )
        },

        async remove (ctx, reviewId) {
            return ctx.dispatch('api/remove',
                { url: ctx.getters.urlPath, id: reviewId }, { root: true }
            )
        },

        async accept (ctx, reviewId) {
            return ctx.dispatch('api/accept',
                { url: ctx.getters.urlPath, data: { id: reviewId } }, { root: true }
            )
        },

        async reject (ctx, reviewId) {
            return ctx.dispatch('api/reject',
                { url: ctx.getters.urlPath, data: { id: reviewId } }, { root: true }
            )
        },
    },
}

/*
    state: () => ({
        review: {
            title: null,
            episode: null,
            header: null,
            created: null,
            body: null,
            user: null,
            isAccepted: null,
            rating: null
        },
        reviews: {
            count: 0,
            next: null,
            previous: null,
            // title, episode, created, header, body, user, isAccepted, rating
            results: []
        }
    }),
 */
