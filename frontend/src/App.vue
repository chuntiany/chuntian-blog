<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <header class="navbar">
    <div class="container nav-container">
      <RouterLink to="/" class="logo">ChunTian' Blog</RouterLink>
      
      <nav>
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        
        <div v-if="authStore.isAuthenticated" class="auth-links">
          <span class="welcome">Hi, {{ authStore.user?.username }}</span>
          <RouterLink to="/admin" v-if="authStore.user?.is_admin" class="nav-link">Admin</RouterLink>
          <button @click="authStore.logout" class="btn-logout">Logout</button>
        </div>
        
        <div v-else class="auth-links">
          <RouterLink to="/login" class="nav-link">Log in</RouterLink>
          <RouterLink to="/register" class="btn-primary">Sign up</RouterLink>
        </div>
      </nav>
    </div>
  </header>

  <main class="main-content">
    <RouterView />
  </main>
</template>

<style scoped>
.navbar {
  background-color: white;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 0.75rem 0;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.logo:hover {
  color: var(--primary-hover);
}

nav {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: var(--text-main);
  font-weight: 500;
}

.nav-link:hover {
  color: var(--primary-color);
}

.auth-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: var(--primary-hover);
  color: white;
}

.btn-logout {
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-main);
  padding: 0.4rem 0.8rem;
}

.btn-logout:hover {
  background-color: #f3f4f6;
  border-color: #d1d5db;
}

.welcome {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.main-content {
  padding-top: 2rem;
  padding-bottom: 4rem;
}
</style>
