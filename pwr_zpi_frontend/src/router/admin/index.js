import {GROUP_ADMIN} from "@/store/group_types";
import {prefixRoutes} from "@/router/helpers";

const admin_routes = {
    path: '/admin',
    component: () => import('../../views/layout/AdminLayout'),
    meta: {
        authRequired: true,
        authGroupRequired: GROUP_ADMIN
    },
    children: [
        {
            path: '',
            name: 'admin',
            component: () => import('../../views/admin/Home')
        },
        {
            path: 'users',
            name: 'admin_users',
            component: () => import('../../views/admin/Users')
        },
        {
            path: 'data/genres',
            name: 'admin_db_genres',
            component: () => import('../../views/admin/db/Genres')
        },
        {
            path: 'data/languages',
            name: 'admin_db_languages',
            component: () => import('../../views/admin/db/Languages')
        },
        {
            path: 'data/countries',
            name: 'admin_db_countries',
            component: () => import('../../views/admin/db/Countries')
        },
        {
            path: 'data/cast-roles',
            name: 'admin_db_cast_roles',
            component: () => import('../../views/admin/db/CastRoles')
        },

        {
            path: 'history/actions',
            name: 'admin_history_actions',
            component: () => import('../../views/admin/history/ActionLogs')
        },
        {
            path: 'history/requests',
            component: () => import('../../views/admin/history/Requests/BaseRequests'),
            children: [
                {
                    path: '',
                    name: 'admin_history_requests',
                    redirect: { name: 'admin_history_requests_title' }
                },
                ...prefixRoutes('title', [
                    {
                        path: '',
                        name: 'admin_history_requests_title',
                        component: () => import('@/views/admin/history/Requests/RequestsTitle')
                    },
                    {
                        path: ':id',
                        name: 'admin_history_requests_title_one',
                        component: () => import('@/views/mod/queue/TitleRequestOne')
                    },
                ]),
                ...prefixRoutes('episode', [
                    {
                        path: '',
                        name: 'admin_history_requests_episode',
                        component: () => import('@/views/admin/history/Requests/RequestsEpisode')
                    },
                    {
                        path: ':id',
                        name: 'admin_history_requests_episode_one',
                        component: () => import('@/views/mod/queue/EpisodeRequestOne')
                    },
                ]),
                ...prefixRoutes('person', [
                    {
                        path: '',
                        name: 'admin_history_requests_person',
                        component: () => import('@/views/admin/history/Requests/RequestsPerson')
                    },
                    {
                        path: ':id',
                        name: 'admin_history_requests_person_one',
                        component: () => import('@/views/mod/queue/PersonRequestOne')
                    },
                ]),
            ],
        },
        {
            path: 'scraper/sites',
            name: 'admin_scraper_sites',
            component: () => import('../../views/admin/scraper/Sites')
        }
    ]
}

export default admin_routes

/*
{
        path: '/admin',
        name: 'admin',
        component: Test,
        children: [
            {
                path: 'users',
                component: Test
            },
            {
                path: 'groups',
                component: Test
            },
            {
                path: 'logs',
                component: Test
            },
            {
                path: 'stats',
                component: Test
            },
            {
                path: 'countries',
                component: Test
            },
            {
                path: 'langs',
                component: Test
            },
            {
                path: 'genres',
                component: Test
            },
            {
                path: 'core',
                component: Test,
                children: [
                    {
                        path: 'email',
                        component: Test
                    },
                    {
                        path: 'login',
                        component: Test
                    },
                ]
            },
        ]
    },
 */