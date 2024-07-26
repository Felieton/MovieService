import storeCfg from '../../config'
import axios from "axios";

export default {
    namespaced: true,
    getters: {
        urlPath() {
            return `${storeCfg.baseUrl}scraper/`
        },

    },

    actions: {
        async getFilmByUrl (ctx, params) {
            return axios.post(ctx.getters.urlPath, params)
        },
    },
}


