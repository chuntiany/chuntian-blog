<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const articles = ref([])
const loading = ref(true)
const router = useRouter()

const fetchArticles = async () => {
  try {
    const response = await axios.get('/api/articles?per_page=100')
    articles.value = response.data.articles
  } catch (error) {
    console.error('Failed to fetch articles', error)
  } finally {
    loading.value = false
  }
}

const deleteArticle = async (id) => {
  if (!confirm('Are you sure you want to delete this article?')) return
  try {
    await axios.delete(`/api/articles/${id}`)
    articles.value = articles.value.filter(a => a.id !== id)
  } catch (error) {
    console.error('Failed to delete article', error)
  }
}

const editArticle = (id) => {
  router.push(`/admin/articles/edit/${id}`)
}

const createArticle = () => {
  router.push('/admin/articles/create')
}

onMounted(fetchArticles)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Articles</h1>
      <button @click="createArticle">New Article</button>
    </div>
    
    <div class="card" v-if="!loading">
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>Category</th>
              <th>Status</th>
              <th>Date</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="article in articles" :key="article.id">
              <td class="title-cell">{{ article.title }}</td>
              <td>{{ article.author }}</td>
              <td><span class="badge" v-if="article.category">{{ article.category }}</span><span v-else>-</span></td>
              <td><span :class="['status-badge', article.status]">{{ article.status }}</span></td>
              <td>{{ new Date(article.created_at).toLocaleDateString() }}</td>
              <td class="actions-cell">
                <button @click="editArticle(article.id)" class="btn-sm secondary">Edit</button>
                <button @click="deleteArticle(article.id)" class="btn-sm danger">Delete</button>
              </td>
            </tr>
            <tr v-if="articles.length === 0">
              <td colspan="6" class="empty-state">No articles found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="loading">Loading...</div>
  </div>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.table-responsive {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-main);
}

tr:last-child td {
  border-bottom: none;
}

.title-cell {
  font-weight: 500;
  color: var(--text-main);
}

.badge {
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.published {
  background-color: #dcfce7;
  color: #166534;
}

.status-badge.draft {
  background-color: #f3f4f6;
  color: #4b5563;
}

.status-badge.private {
  background-color: #fee2e2;
  color: #991b1b;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
}

.btn-sm.secondary {
  background: white;
  border: 1px solid var(--border-color);
  color: var(--text-main);
}

.btn-sm.secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
}

.btn-sm.danger {
  background: white;
  border: 1px solid #fee2e2;
  color: #dc2626;
}

.btn-sm.danger:hover {
  background: #fef2f2;
  border-color: #fca5a5;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
}
</style>
