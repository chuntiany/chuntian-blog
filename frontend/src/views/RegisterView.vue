<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleRegister = async () => {
  const success = await authStore.register(username.value, email.value, password.value)
  if (success) {
    router.push('/login')
  } else {
    error.value = 'Registration failed'
  }
}
</script>

<template>
  <div class="register">
    <h1>Register</h1>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label>Username</label>
        <input v-model="username" type="text" required />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" required />
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<style scoped>
.register {
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
