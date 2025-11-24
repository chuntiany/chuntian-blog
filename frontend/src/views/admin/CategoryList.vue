<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const categories = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingCategory = ref(null)
const form = ref({ name: '', description: '' })

const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/categories')
    categories.value = response.data
  } catch (error) {
    console.error('Failed to fetch categories', error)
  } finally {
    loading.value = false
  }
}

const openCreateModal = () => {
  editingCategory.value = null
  form.value = { name: '', description: '' }
  showModal.value = true
}

const openEditModal = (category) => {
  editingCategory.value = category
  form.value = { name: category.name, description: category.description }
  showModal.value = true
}

const saveCategory = async () => {
  try {
    if (editingCategory.value) {
      await axios.put(`/api/categories/${editingCategory.value.id}`, form.value)
    } else {
      await axios.post('/api/categories', form.value)
    }
    await fetchCategories()
    showModal.value = false
  } catch (error) {
    console.error('Failed to save category', error)
    alert('Failed to save category')
  }
}

const deleteCategory = async (id) => {
  if (!confirm('Are you sure?')) return
  try {
    await axios.delete(`/api/categories/${id}`)
    await fetchCategories()
  } catch (error) {
    console.error('Failed to delete category', error)
    alert(error.response?.data?.error || 'Failed to delete')
  }
}

onMounted(fetchCategories)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Categories</h1>
      <button @click="openCreateModal">New Category</button>
    </div>
    
    <div class="card" v-if="!loading">
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Articles</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="category in categories" :key="category.id">
              <td class="name-cell">{{ category.name }}</td>
              <td>{{ category.description }}</td>
              <td><span class="badge">{{ category.article_count }}</span></td>
              <td class="actions-cell">
                <button @click="openEditModal(category)" class="btn-sm secondary">Edit</button>
                <button @click="deleteCategory(category.id)" class="btn-sm danger">Delete</button>
              </td>
            </tr>
            <tr v-if="categories.length === 0">
              <td colspan="4" class="empty-state">No categories found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else class="loading">Loading...</div>
    
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-card">
        <h2>{{ editingCategory ? 'Edit' : 'New' }} Category</h2>
        <form @submit.prevent="saveCategory">
          <div class="form-group">
            <label>Name</label>
            <input v-model="form.name" required placeholder="Category name" />
          </div>
          <div class="form-group">
            <label>Description</label>
            <input v-model="form.description" placeholder="Short description" />
          </div>
          <div class="form-actions">
            <button type="button" class="secondary" @click="showModal = false">Cancel</button>
            <button type="submit">Save</button>
          </div>
        </form>
      </div>
    </div>
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

.name-cell {
  font-weight: 500;
}

.badge {
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
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

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 100%;
  max-width: 450px;
  box-shadow: var(--shadow-md);
}

.modal-card h2 {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  box-sizing: border-box;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

button.secondary {
  background: white;
  border: 1px solid var(--border-color);
  color: var(--text-main);
}

button.secondary:hover {
  background: #f9fafb;
}
</style>
