import mod_routes from "./mod";
import admin_routes from "./admin";
import {GROUP_USER} from "@/store/group_types";
import store from "../store";

const routes = [
    {
        path: '/',
        component: () => import('../views/layout/MainLayout'),
        children: [
            {
                path: '',
                component: () => import('../views/Home.vue')
            },
            {
                path: 'add',
                component: () => import('../views/adding/BaseAdd.vue'),
                meta: {
                    authRequired: true,
                    authGroupRequired: GROUP_USER
                },
                children: [
                    {
                        path: '',
                        name: "Add",
                        component: () => import('../views/adding/Add'),
                    },
                    {
                        path: 'title',
                        name: "AddTitle",
                        component: () => import('../views/adding/AddTitle'),
                    },
                    {
                        path: 'episode',
                        name: "AddEpisode",
                        component: () => import('../views/adding/AddEpisode'),
                    },
                    {
                        path: 'person',
                        name: "AddPerson",
                        component: () => import('../views/adding/AddPerson'),
                    },
                ]
            },
            {
                path: 'login',
                name: "Login",
                component: () => import('../views/security/Login.vue')
            },
            {
                path: 'user/:id',
                component: () => import('../views/user/BaseUser'),
                meta: {
                    authRequired: true,
                    authGroupRequired: GROUP_USER
                },
                children: [
                    {
                        path: '',
                        name: "UserProfile",
                        component: () => import('../views/user/User'),
                    },
                    {
                        path: 'reviews',
                        name: 'user_reviews',
                        component: () => import('../views/user/UserReviews')
                    },
                    {
                        path: 'episode-reviews',
                        name: 'user_episode_reviews',
                        component: () => import('../views/user/UserEpisodeReviews')
                    },
                    {
                        path: 'watchlist',
                        name: 'user_watchlist',
                        component: () => import('../views/user/UserWatchlist')
                    },
                    {
                        path: 'settings',
                        name: 'user_settings',
                        component: () => import('../views/user/UserSettings'),
                        beforeEnter: (to, from, next) => {
                            if (store.getters.loggedUser.id == to.params.id) {
                                next()
                            }
                            else
                                next(new Error("Access denied"))
                        }
                    },
                ]
            },
            {
                path: 'movies',
                component: () => import('../views/movies/Movies'),
            },
            {
                path: 'movies/:id',
                component: () => import('../views/movies/BaseMovie'),
                children: [
                    {
                        path: '',
                        name: "movies_single",
                        component: () => import('../views/movies/Movie'),
                    },
                    {
                        path: 'reviews',
                        name: "movie_reviews",
                        component: () => import('../views/movies/MovieReviews')
                    }
                ]
            },
            {
                path: 'series/:id',
                component: () => import('../views/series/BaseSingleSeries'),
                children: [
                    {
                        path: '',
                        name: "series_single",
                        component: () => import('../views/series/SingleSeries'),
                    },
                    {
                        path: 'reviews',
                        name: "series_reviews",
                        component: () => import('../views/series/SeriesReviews')
                    },
                    {
                        path: 'episodes',
                        component: () => import('../views/series/episodes/BaseEpisodes'),
                        children: [
                            {
                                path: '',
                                name: "series_episodes",
                                component: () => import('../views/series/episodes/Episodes')
                            },
                            {
                                path: ':epid',
                                component: () => import('../views/series/episodes/BaseEpisode'),
                                children: [
                                    {
                                        path: '',
                                        name: "episode_single",
                                        component: () => import('../views/series/episodes/Episode'),
                                    },
                                    {
                                        path: 'reviews',
                                        name: "episode_reviews",
                                        component: () => import('../views/series/episodes/EpisodeReviews')
                                    },
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                path: 'people/:id',
                name: 'people_single',
                component: () => import('../views/people/Person'),
            },
            {
                path: 'series',
                component: () => import('../views/series/Series'),
            },
            {
                path: 'people',
                component: () => import('../views/people/People'),
            },
            {
                path: 'privacy-policy',
            },
            {
                path: 'about-us',
            },
            {
                path: 'contact',
            },
        ]
    },
    mod_routes,
    admin_routes,
    {
        path: '/email-sent',
        name: 'EmailSent',
        component: () => import('../views/security/EmailSent')
    },
    {
        path: '/verification/:key',
        name: 'Verification',
        component: () => import('../views/security/EmailVerification')
    },
]

export default routes
