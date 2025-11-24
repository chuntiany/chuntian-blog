import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')) || null,
        isAuthenticated: !!localStorage.getItem('user')
    }),
    actions: {
        async login(username, password) {
            try {
                const response = await axios.post('/auth/login', { username, password })
                this.user = response.data.user
                this.isAuthenticated = true
                localStorage.setItem('user', JSON.stringify(this.user))
                return true
            } catch (error) {
                console.error('Login failed', error)
                return false
            }
        },
        async register(username, email, password) {
            try {
                await axios.post('/auth/register', { username, email, password })
                return true
            } catch (error) {
                console.error('Registration failed', error)
                return false
            }
        },
        async logout() {
            try {
                await axios.post('/auth/logout')
            } catch (error) {
                console.error('Logout failed', error)
            } finally {
                this.user = null
                this.isAuthenticated = false
                localStorage.removeItem('user')
            }
        }
    }
})
