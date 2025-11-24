<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const articles = ref([])
const categories = ref([])
const loading = ref(true)
const searchQuery = ref('')
const selectedCategory = ref(null)

const fetchData = async () => {
  console.log('Fetching data...')
  try {
    const [articlesRes, categoriesRes] = await Promise.all([
      axios.get('/api/articles'),
      axios.get('/api/categories')
    ])
    console.log('Data fetched:', articlesRes.data, categoriesRes.data)
    articles.value = articlesRes.data.articles
    categories.value = categoriesRes.data
  } catch (error) {
    console.error('Failed to fetch data', error)
  } finally {
    console.log('Setting loading to false')
    loading.value = false
  }
}

const filteredArticles = computed(() => {
  return articles.value.filter(article => {
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          article.summary.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value ? article.category === selectedCategory.value : true
    return matchesSearch && matchesCategory
  })
})

const selectCategory = (categoryName) => {
  selectedCategory.value = categoryName
}

onMounted(fetchData)
</script>

<template>
  <div class="container home-layout">
    <aside class="sidebar">
      <div class="card category-card">
        <h3>Categories</h3>
        <ul class="category-list">
          <li :class="{ active: !selectedCategory }">
            <a href="#" @click.prevent="selectCategory(null)">All Categories</a>
          </li>
          <li v-for="cat in categories" :key="cat.id" :class="{ active: selectedCategory === cat.name }">
            <a href="#" @click.prevent="selectCategory(cat.name)">{{ cat.name }}</a>
          </li>
        </ul>
      </div>
    </aside>

    <main class="feed">
      <div class="card search-card">
        <h3>Search</h3>
        <div class="search-input-wrapper">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search articles..." 
            class="search-input"
          />
        </div>
      </div>

      <div v-if="loading" class="loading">Loading...</div>
      
      <div v-else class="articles-list">
        <div v-for="article in filteredArticles" :key="article.id" class="card article-card">
          <div class="card-header">
            <span class="tag" v-if="article.category">{{ article.category }}</span>
            <span class="date">{{ new Date(article.created_at).toLocaleDateString() }}</span>
          </div>
          
          <h2 class="article-title">
            <router-link :to="'/article/' + article.id">{{ article.title }}</router-link>
          </h2>
          
          <p class="article-summary">{{ article.summary }}</p>
          
          <div class="card-footer">
            <div class="author">
              <span class="author-name">By {{ article.author }}</span>
            </div>
            <router-link :to="'/article/' + article.id" class="read-more">
              Read more →
            </router-link>
          </div>
        </div>
        
        <div v-if="filteredArticles.length === 0" class="no-results">
          No articles found.
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
  align-items: start;
}

@media (max-width: 768px) {
  .home-layout {
    grid-template-columns: 1fr;
  }
}

/* Sidebar */
.category-card h3 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-list li {
  margin-bottom: 0.5rem;
}

.category-list a {
  display: block;
  padding: 0.5rem;
  color: var(--text-main);
  border-radius: 6px;
  transition: background-color 0.2s, color 0.2s;
}

.category-list a:hover {
  background-color: #f3f4f6;
  color: var(--primary-color);
}

.category-list li.active a {
  background-color: #eff6ff;
  color: var(--primary-color);
  font-weight: 500;
}

/* Feed */
.feed {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.search-card h3 {
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

/* Article Card */
.article-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.tag {
  background-color: #eff6ff;
  color: var(--primary-color);
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
}

.date {
  color: var(--text-muted);
  font-size: 0.85rem;
}

.article-title {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.article-title a {
  color: var(--text-main);
}

.article-title a:hover {
  color: var(--primary-color);
}

.article-summary {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f3f4f6;
  padding-top: 1rem;
}

.author-name {
  font-size: 0.9rem;
  color: var(--text-main);
  font-weight: 500;
}

.read-more {
  font-size: 0.9rem;
  font-weight: 500;
}

.no-results {
  text-align: center;
  color: var(--text-muted);
  padding: 2rem;
}
</style>
