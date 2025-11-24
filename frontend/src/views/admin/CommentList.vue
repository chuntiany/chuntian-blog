<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const comments = ref([])
const loading = ref(true)
const filterStatus = ref('')

const fetchComments = async () => {
  loading.value = true
  try {
    const url = filterStatus.value ? `/api/comments?status=${filterStatus.value}` : '/api/comments'
    const response = await axios.get(url)
    comments.value = response.data
  } catch (error) {
    console.error('Failed to fetch comments', error)
  } finally {
    loading.value = false
  }
}

const updateStatus = async (id, status) => {
  try {
    await axios.put(`/api/comments/${id}/status`, { status })
    await fetchComments()
  } catch (error) {
    console.error('Failed to update status', error)
  }
}

const deleteComment = async (id) => {
  if (!confirm('Are you sure?')) return
  try {
    await axios.delete(`/api/comments/${id}`)
    await fetchComments()
  } catch (error) {
    console.error('Failed to delete comment', error)
  }
}

onMounted(fetchComments)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Comments</h1>
      <select v-model="filterStatus" @change="fetchComments" class="filter-select">
        <option value="">All Status</option>
        <option value="pending">Pending</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
      </select>
    </div>
    
    <div class="card" v-if="!loading">
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Author</th>
              <th>Content</th>
              <th>Article ID</th>
              <th>Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="comment in comments" :key="comment.id">
              <td class="author-cell">{{ comment.author }}</td>
              <td class="content-cell">{{ comment.content }}</td>
              <td>{{ comment.article_id }}</td>
              <td>{{ new Date(comment.created_at).toLocaleDateString() }}</td>
              <td><span :class="['status-badge', comment.status]">{{ comment.status }}</span></td>
              <td class="actions-cell">
                <button v-if="comment.status !== 'approved'" @click="updateStatus(comment.id, 'approved')" class="btn-sm success">Approve</button>
                <button v-if="comment.status !== 'rejected'" @click="updateStatus(comment.id, 'rejected')" class="btn-sm warning">Reject</button>
                <button @click="deleteComment(comment.id)" class="btn-sm danger">Delete</button>
              </td>
            </tr>
            <tr v-if="comments.length === 0">
              <td colspan="6" class="empty-state">No comments found.</td>
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

.filter-select {
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: white;
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
  vertical-align: top;
}

tr:last-child td {
  border-bottom: none;
}

.author-cell {
  font-weight: 500;
  white-space: nowrap;
}

.content-cell {
  max-width: 300px;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.approved {
  background-color: #dcfce7;
  color: #166534;
}

.status-badge.pending {
  background-color: #fef9c3;
  color: #854d0e;
}

.status-badge.rejected {
  background-color: #fee2e2;
  color: #991b1b;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.btn-sm.success {
  background-color: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.btn-sm.success:hover {
  background-color: #bbf7d0;
}

.btn-sm.warning {
  background-color: #fef9c3;
  color: #854d0e;
  border: 1px solid #fde047;
}

.btn-sm.warning:hover {
  background-color: #fde047;
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
