<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  const success = await authStore.login(username.value, password.value)
  if (success) {
    router.push('/')
  } else {
    error.value = 'Invalid username or password'
  }
}
</script>

<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>Username</label>
        <input v-model="username" type="text" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" required />
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
}
input {
  width: 100%;
  padding: 0.5rem;
}
.error {
  color: red;
  margin-bottom: 1rem;
}
</style>
