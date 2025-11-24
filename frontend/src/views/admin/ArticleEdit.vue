<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const isEdit = route.params.id !== undefined
const loading = ref(isEdit)
const categories = ref([])

const form = ref({
  title: '',
  summary: '',
  content: '',
  category_id: null,
  status: 'published'
})

const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/categories')
    categories.value = response.data
  } catch (error) {
    console.error('Failed to fetch categories', error)
  }
}

const fetchArticle = async () => {
  try {
    const response = await axios.get(`/api/articles/${route.params.id}`)
    const article = response.data
    form.value = {
      title: article.title,
      summary: article.summary,
      content: article.content,
      category_id: article.category_id,
      status: article.status
    }
  } catch (error) {
    console.error('Failed to fetch article', error)
  } finally {
    loading.value = false
  }
}

const saveArticle = async () => {
  try {
    if (isEdit) {
      await axios.put(`/api/articles/${route.params.id}`, form.value)
    } else {
      await axios.post('/api/articles', form.value)
    }
    router.push('/admin/articles')
  } catch (error) {
    console.error('Failed to save article', error)
    alert('Failed to save article')
  }
}

onMounted(async () => {
  await fetchCategories()
  if (isEdit) {
    await fetchArticle()
  }
})
</script>

<template>
  <div>
    <div class="page-header">
      <h1>{{ isEdit ? 'Edit Article' : 'New Article' }}</h1>
    </div>
    
    <div class="card" v-if="!loading">
      <form @submit.prevent="saveArticle">
        <div class="form-group">
          <label>Title</label>
          <input v-model="form.title" required placeholder="Enter article title" />
        </div>
        
        <div class="form-row">
          <div class="form-group half">
            <label>Category</label>
            <select v-model="form.category_id">
              <option :value="null">Uncategorized</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          
          <div class="form-group half">
            <label>Status</label>
            <select v-model="form.status">
              <option value="published">Published</option>
              <option value="draft">Draft</option>
              <option value="private">Private</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label>Summary</label>
          <textarea v-model="form.summary" rows="3" placeholder="Brief summary of the article"></textarea>
        </div>
        
        <div class="form-group">
          <label>Content (Markdown)</label>
          <textarea v-model="form.content" rows="20" required placeholder="Write your article content here..."></textarea>
        </div>
        
        <div class="form-actions">
          <button type="button" class="secondary" @click="router.back()">Cancel</button>
          <button type="submit">Save Article</button>
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

.form-row {
  display: flex;
  gap: 1.5rem;
}

.half {
  flex: 1;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-main);
}

input, select, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.95rem;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

button.secondary {
  background: white;
  border: 1px solid var(--border-color);
  color: var(--text-main);
}

button.secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}
</style>
