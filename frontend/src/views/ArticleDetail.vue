<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const route = useRoute()
const authStore = useAuthStore()
const article = ref(null)
const loading = ref(true)
const commentContent = ref('')
const comments = ref([])
const headings = ref([])

const renderedContent = computed(() => {
  if (!article.value || !article.value.content) return ''
  const rawHtml = marked.parse(article.value.content)
  return DOMPurify.sanitize(rawHtml)
})

const extractHeadings = () => {
  if (!article.value || !article.value.content) return
  const tokens = marked.lexer(article.value.content)
  const extracted = []
  tokens.forEach(token => {
    if (token.type === 'heading') {
      const slug = token.text.toLowerCase().replace(/[^\w]+/g, '-')
      extracted.push({
        text: token.text,
        depth: token.depth,
        slug: slug
      })
    }
  })
  headings.value = extracted
}

// Custom renderer to add IDs to headings
const renderer = new marked.Renderer()
renderer.heading = ({ text, depth }) => {
  const slug = text.toLowerCase().replace(/[^\w]+/g, '-')
  return `<h${depth} id="${slug}">${text}</h${depth}>`
}
marked.use({ renderer })

const fetchArticle = async () => {
  try {
    const response = await axios.get(`/api/articles/${route.params.id}`)
    article.value = response.data
    extractHeadings()
  } catch (error) {
    console.error('Failed to fetch article', error)
  }
}

const fetchComments = async () => {
  try {
    const response = await axios.get(`/api/comments?article_id=${route.params.id}`)
    comments.value = response.data
  } catch (error) {
    console.error('Failed to fetch comments', error)
  }
}

const submitComment = async () => {
  if (!commentContent.value.trim()) return
  
  try {
    const response = await axios.post('/api/comments', {
      content: commentContent.value,
      article_id: article.value.id
    })
    
    if (response.data.status === 'approved') {
      comments.value.unshift({
        id: response.data.id,
        content: commentContent.value,
        author: authStore.user.username,
        created_at: new Date().toISOString()
      })
    } else {
      alert('Comment submitted for approval')
    }
    commentContent.value = ''
  } catch (error) {
    console.error('Failed to submit comment', error)
    alert('Failed to submit comment')
  }
}

const scrollToHeading = (slug) => {
  const element = document.getElementById(slug)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(async () => {
  await fetchArticle()
  await fetchComments()
  loading.value = false
})
</script>

<template>
  <div class="container article-layout" v-if="!loading && article">
    <main class="article-content-wrapper">
      <div class="card article-detail">
        <h1 class="title">{{ article.title }}</h1>
        <div class="meta">
          <span>By {{ article.author }}</span>
          <span> | {{ new Date(article.created_at).toLocaleDateString() }}</span>
          <span v-if="article.category"> | {{ article.category }}</span>
        </div>
        
        <div class="content markdown-body" v-html="renderedContent"></div>
        
        <div class="comments-section">
          <h3>Comments</h3>
          
          <div v-if="authStore.isAuthenticated" class="comment-form">
            <textarea v-model="commentContent" placeholder="Write a comment..." rows="3"></textarea>
            <button @click="submitComment">Post Comment</button>
          </div>
          <div v-else>
            <router-link to="/login">Login to comment</router-link>
          </div>
          
          <div class="comments-list">
            <div v-for="comment in comments" :key="comment.id" class="comment">
              <p><strong>{{ comment.author }}</strong> said:</p>
              <p>{{ comment.content }}</p>
              <small>{{ new Date(comment.created_at).toLocaleDateString() }}</small>
            </div>
            <div v-if="comments.length === 0">No comments yet.</div>
          </div>
        </div>
      </div>
    </main>

    <aside class="sidebar">
      <div class="card toc-card" v-if="headings.length > 0">
        <h3>Table of Contents</h3>
        <ul class="toc-list">
          <li v-for="heading in headings" :key="heading.slug" :class="'depth-' + heading.depth">
            <a href="#" @click.prevent="scrollToHeading(heading.slug)">{{ heading.text }}</a>
          </li>
        </ul>
      </div>
    </aside>
  </div>
  <div v-else-if="!loading">Article not found</div>
  <div v-else>Loading...</div>
</template>

<style scoped>
.article-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 960px) {
  .article-layout {
    grid-template-columns: 1fr;
  }
  .sidebar {
    display: none;
  }
}

.article-detail {
  background: white;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.title {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.meta {
  color: var(--text-muted);
  margin-bottom: 2rem;
  font-size: 0.95rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

.content {
  line-height: 1.8;
  font-size: 1.1em;
  margin-bottom: 3rem;
  color: var(--text-main);
}

/* TOC Styles */
.toc-card {
  position: sticky;
  top: 5rem; /* Adjust based on navbar height */
}

.toc-card h3 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-list li {
  margin-bottom: 0.5rem;
}

.toc-list a {
  display: block;
  padding: 0.25rem 0;
  color: var(--text-muted);
  font-size: 0.95rem;
  transition: color 0.2s;
  text-decoration: none;
}

.toc-list a:hover {
  color: var(--primary-color);
}

.depth-1 { padding-left: 0; font-weight: 600; }
.depth-2 { padding-left: 1rem; }
.depth-3 { padding-left: 2rem; font-size: 0.9rem; }
.depth-4 { padding-left: 3rem; font-size: 0.9rem; }

/* Markdown Styles */
:deep(.markdown-body h1),
:deep(.markdown-body h2),
:deep(.markdown-body h3) {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
  scroll-margin-top: 6rem; /* For sticky navbar */
}

:deep(.markdown-body p) {
  margin-bottom: 1em;
}

:deep(.markdown-body ul),
:deep(.markdown-body ol) {
  padding-left: 1.5em;
  margin-bottom: 1em;
}

:deep(.markdown-body code) {
  background-color: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9em;
}

:deep(.markdown-body pre) {
  background-color: #1f2937;
  color: #f3f4f6;
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 1.5em;
}

:deep(.markdown-body pre code) {
  background-color: transparent;
  padding: 0;
  color: inherit;
}

:deep(.markdown-body blockquote) {
  border-left: 4px solid var(--primary-color);
  padding-left: 1rem;
  margin-left: 0;
  color: var(--text-muted);
  font-style: italic;
}

.comments-section {
  border-top: 1px solid var(--border-color);
  padding-top: 2rem;
}

.comment-form {
  margin-bottom: 2rem;
}

textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  margin-bottom: 0.5rem;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
}

textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

.comment {
  border-bottom: 1px solid #f9f9f9;
  padding: 1rem 0;
}

.comment:last-child {
  border-bottom: none;
}
</style>
