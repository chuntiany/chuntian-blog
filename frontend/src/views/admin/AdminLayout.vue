<script setup>
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const route = useRoute()

const isActive = (path) => route.path === path
</script>

<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <h2>Admin Panel</h2>
      </div>
      <nav class="sidebar-nav">
        <RouterLink to="/admin" :class="{ active: isActive('/admin') }">
          Dashboard
        </RouterLink>
        <RouterLink to="/admin/articles" :class="{ active: route.path.startsWith('/admin/articles') }">
          Articles
        </RouterLink>
        <RouterLink to="/admin/categories" :class="{ active: route.path.startsWith('/admin/categories') }">
          Categories
        </RouterLink>
        <RouterLink to="/admin/comments" :class="{ active: route.path.startsWith('/admin/comments') }">
          Comments
        </RouterLink>
        <RouterLink to="/admin/settings" :class="{ active: route.path.startsWith('/admin/settings') }">
          Settings
        </RouterLink>
        
        <div class="divider"></div>
        
        <RouterLink to="/">Back to Site</RouterLink>
        <a href="#" @click.prevent="authStore.logout" class="logout">Logout</a>
      </nav>
    </aside>
    <main class="admin-content">
      <div class="container">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-color);
}

.admin-sidebar {
  width: 260px;
  background: white;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  top: 0;
  left: 0;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-header h2 {
  font-size: 1.25rem;
  color: var(--text-main);
}

.sidebar-nav {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sidebar-nav a {
  padding: 0.75rem 1rem;
  color: var(--text-muted);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
  font-weight: 500;
}

.sidebar-nav a:hover {
  background-color: #f3f4f6;
  color: var(--text-main);
}

.sidebar-nav a.active {
  background-color: #eff6ff;
  color: var(--primary-color);
}

.divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 1rem 0;
}

.logout {
  color: #dc2626 !important;
}

.logout:hover {
  background-color: #fef2f2 !important;
  color: #b91c1c !important;
}

.admin-content {
  flex: 1;
  margin-left: 260px; /* Width of sidebar */
  padding: 2rem;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
