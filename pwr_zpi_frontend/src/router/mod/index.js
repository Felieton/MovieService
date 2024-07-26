import {prefixRoutes} from "@/router/helpers";
import {GROUP_MOD} from "@/store/group_types";

const mod_routes = {
    path: '/mod',
    component: () => import('@/views/layout/MainLayout'),
    meta: {
        authRequired: true,
        authGroupRequired: GROUP_MOD
    },
    children: [
        {
            path: '',
            component: () => import('@/views/mod/BaseMod'),
            children: [
                {
                    path: '',
                    name: 'mod',
                    redirect: { name: 'mod_queue_reviews' }
                },
                ...prefixRoutes('queue', [
                    {
                        path: '',
                        redirect: { name: 'mod_queue_reviews' }
                    },
                    {
                        path: 'reviews',
                        name: 'mod_queue_reviews',
                        component: () => import('@/views/mod/queue/Reviews')
                    },
                    ...prefixRoutes('title-requests', [
                        {
                            path: '',
                            name: 'mod_queue_title',
                            component: () => import('@/views/mod/queue/TitleRequest')
                        },
                        {
                            path: ':id',
                            name: 'mod_queue_title_one',
                            component: () => import('@/views/mod/queue/TitleRequestOne')
                        },
                    ]),
                    ...prefixRoutes('episode-requests', [
                        {
                            path: '',
                            name: 'mod_queue_episode',
                            component: () => import('@/views/mod/queue/EpisodeRequest')
                        },
                        {
                            path: ':id',
                            name: 'mod_queue_episode_one',
                            component: () => import('@/views/mod/queue/EpisodeRequestOne')
                        },
                    ]),
                    ...prefixRoutes('person-requests', [
                        {
                            path: '',
                            name: 'mod_queue_person',
                            component: () => import('@/views/mod/queue/PersonRequest')
                        },
                        {
                            path: ':id',
                            name: 'mod_queue_person_one',
                            component: () => import('@/views/mod/queue/PersonRequestOne')
                        },
                    ])
                ])
            ],
        },
    ]
}

export default mod_routes

/*
{
        path: '/mod',
        name: 'mod_control_panel',
        component: Test,
        children: [
            {
                path: 'queue/reviews',
                component: Test
            },
            {
                path: 'queue/title-requests',
                component: Test
            },
            {
                path: 'queue/episode-requests',
                component: Test
            },
            {
                path: 'queue/person-requests',
                component: Test
            },
        ]
    },
 */