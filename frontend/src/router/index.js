import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView
        },
        {
            path: '/register',
            name: 'register',
            component: RegisterView
        },
        {
            path: '/article/:id',
            name: 'article-detail',
            component: () => import('../views/ArticleDetail.vue')
        },
        {
            path: '/admin',
            component: () => import('../views/admin/AdminLayout.vue'),
            meta: { requiresAuth: true, requiresAdmin: true },
            children: [
                {
                    path: '',
                    name: 'admin-dashboard',
                    component: () => import('../views/admin/DashboardView.vue')
                },
                {
                    path: 'articles',
                    name: 'admin-articles',
                    component: () => import('../views/admin/ArticleList.vue')
                },
                {
                    path: 'articles/create',
                    name: 'admin-article-create',
                    component: () => import('../views/admin/ArticleEdit.vue')
                },
                {
                    path: 'articles/edit/:id',
                    name: 'admin-article-edit',
                    component: () => import('../views/admin/ArticleEdit.vue')
                },
                {
                    path: 'categories',
                    name: 'admin-categories',
                    component: () => import('../views/admin/CategoryList.vue')
                },
                {
                    path: 'comments',
                    name: 'admin-comments',
                    component: () => import('../views/admin/CommentList.vue')
                },
                {
                    path: 'settings',
                    name: 'admin-settings',
                    component: () => import('../views/admin/SettingsView.vue')
                }
            ]
        }
    ]
})

import { useAuthStore } from '../stores/auth'

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login')
    } else if (to.meta.requiresAdmin && !authStore.user?.is_admin) {
        next('/')
    } else {
        next()
    }
})

export default router
