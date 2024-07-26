import actionLog from './actionLog'
import castMember from './castMember'
import castRole from './castRole'
import character from './character'
import country from './country'
import episode from './episode'
import episodeRequest from './episodeRequest'
import episodeSubmission from './episodeSubmission'
import genre from './genre'
import group from './group'
import lang from './lang'
import permission from './permission'
import person from './person'
import personRequest from './personRequest'
import personSubmission from './personSubmission'
import requestLog from './requestLog'
import review from './review'
import title from './title'
import titleRequest from './titleRequest'
import titleSubmission from './titleSubmission'
import user from './user'
import scraper from './scraper'
import scraperSite from './scraperSite'
import axios from "axios";

export default {
    namespaced: true,
    actions: {
        async loadOne (ctx, {url, id}) {
            return axios.get(`${url}${id}/`)
        },
        async loadMany (ctx, { url, params}) {
            return axios.get(`${url}`, {params})
        },
        async create (ctx, { url, newObject }) {
            return axios.post(`${url}`, newObject)
        },
        async update (ctx, { url, partialObject}) {
            const id = partialObject.id
            delete partialObject.id
            let formData = undefined
            if ('file' in partialObject) {
                formData = new FormData()
                formData.append(partialObject.file.name, partialObject.file.content)
                for (const [key, value] of Object.entries(partialObject)) {
                    if (key !== 'file') {
                        formData.append(key, value)
                    }
                }
            }
            if (formData) return axios.patch(
                `${url}${id}/`,
                formData,
                {
                    headers: { 'Content-Type': 'multipart/form-data' }
                }
            )
            else return axios.patch(`${url}${id}/`, partialObject)
        },
        async remove (ctx, { url, id }) {
            return axios.delete(`${url}${id}/`)
        },
        async accept (ctx, {url, data}) {
            const id = data.id
            delete data.id
            return axios.post(`${url}${id}/accept/`, data)
        },
        async reject (ctx, {url, data}) {
            const id = data.id
            delete data.id
            return axios.post(`${url}${id}/reject/`, data)
        },
    },

    modules: {
        actionLog,
        castMember,
        castRole,
        character,
        country,
        episode,
        episodeRequest,
        episodeSubmission,
        genre,
        group,
        lang,
        permission,
        person,
        personRequest,
        personSubmission,
        requestLog,
        review,
        title,
        titleRequest,
        titleSubmission,
        user,
        scraper,
        scraperSite
    }
}
