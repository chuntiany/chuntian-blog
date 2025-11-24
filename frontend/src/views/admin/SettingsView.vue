<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const settings = ref({})
const loading = ref(true)

const fetchSettings = async () => {
  try {
    const response = await axios.get('/api/settings')
    settings.value = response.data
  } catch (error) {
    console.error('Failed to fetch settings', error)
  } finally {
    loading.value = false
  }
}

const saveSettings = async () => {
  try {
    await axios.post('/api/settings', settings.value)
    alert('Settings saved successfully')
  } catch (error) {
    console.error('Failed to save settings', error)
    alert('Failed to save settings')
  }
}

onMounted(fetchSettings)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Settings</h1>
    </div>
    
    <div class="card" v-if="!loading">
      <form @submit.prevent="saveSettings">
        <div class="form-group">
          <label>Site Title</label>
          <input v-model="settings.site_title" placeholder="My Blog" />
          <small>The title that appears in the browser tab and navigation bar.</small>
        </div>
        
        <div class="form-group">
          <label>Allow Comments</label>
          <select v-model="settings.allow_comments">
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
          <small>Enable or disable comments globally.</small>
        </div>
        
        <div class="form-actions">
          <button type="submit">Save Settings</button>
        </div>
      </form>
    </div>
    <div v-else class="loading">Loading...</div>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input, select {
  width: 100%;
  max-width: 500px;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  box-sizing: border-box;
}

small {
  display: block;
  margin-top: 0.5rem;
  color: var(--text-muted);
}

.form-actions {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}
</style>
