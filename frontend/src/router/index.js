import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'mainPane',
            component: () => import('@/views/mainpane/mainPane.vue'),
            meta: {
                // requireNotAuth: true,
            },
        },
        {
            path: '/login',
            name: 'loginPane',
            component: () => import('@/views/accountpane/loginPane.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path: '/register',
            name: 'registerPane',
            component: () => import('@/views/accountpane/registerPane.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path: '/accountCenter',
            name: 'accountCenter',
            component: () => import('@/views/accountpane/accountCenter.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionairemanage',
            name:'questionairemanage',
            component: () => import('@/views/qn-manage/qnManage.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionairecollect',
            name:'questionairecollect',
            component: () => import('@/views/qn-manage/qnCollect.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionairehistory',
            name:'questionairehistory',
            component: () => import('@/views/qn-manage/qnHistory.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionaireCreate',
            name:'questionaireCreate',
            component: () => import('@/views/qn-createpane/qnCreate.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionaireEdit/:qnid',
            name:'questionaireEdit',
            component: () => import('@/views/qn-createpane/qn-modelPane/qnEdit.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionaireEditTest/:qnid',
            name:'questionaireEditTest',
            component: () => import('@/views/qn-createpane/qn-modelPane/qnEditTest.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionaireEditVote/:qnid',
            name:'questionaireEditVote',
            component: () => import('@/views/qn-createpane/qn-modelPane/qnEditVote.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionaireRecycle',
            name:'questionaireRecycle',
            component: () => import('@/views/qn-manage/qnRecycle.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionaireCollect',
            name:'questionaireCollect',
            component: () => import('@/views/qn-manage/qnCollect.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionaireDataview/:qnid',
            name:'questionaireDataview',
            component: () => import('@/views/qn-data/qnTestDataview.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        
        {
            path:'/questionaireTest',
            name:'questionaireTest',
            component: () => import('@/views/qn-createpane/qn-modelPane/qnEditTest.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionaireVote',
            name:'questionaireVote',
            component: () => import('@/views/qn-createpane/qn-modelPane/qnEditVote.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/fillQn/:code',
            name:'fillQn',
            component: () => import('@/views/qn-fillpane/fillQn.vue'),
            meta: {
                noNav: false
            },
        },
        {
            path:'/fillQnmycheckin',
            name:'fillQnmycheckin',
            component: () => import('@/views/qn-fillpane/fillQnmycheckin.vue'),
            meta: {
                noNav: false
            },
        },
        {
            path:'/fillQnmytest/:code',
            name:'fillQnmytest',
            component: () => import('@/views/qn-fillpane/fillQnmytest.vue'),
            meta: {
                noNav: false
            },
        },
        {
            path:'/fillQnmyvote/:code',
            name:'fillQnmyvote',
            component: () => import('@/views/qn-fillpane/fillQnmyvote.vue'),
            meta: {
                noNav: false
            },
        },
        {
            path:'/testAnalysis/:qnid',
            name:'testAnalysis',
            component: () => import('@/views/qn-data/qnAnalysis.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionnaireSquare',
            name:'questionnaireSquare',
            component: () => import('@/views/qn-manage/qnSquare.vue'),
            meta: {
                requireNotAuth: true,
                noNav: true
            },
        },
        {
            path:'/questionnaireSquareTest',
            name:'questionnaireSquareTest',
            component: () => import('@/views/qn-manage/qnSquareTest.vue'),
            meta: {
                requireNotAuth: true,
                noNav: false
            },
        },
    ]
});

export default router;
