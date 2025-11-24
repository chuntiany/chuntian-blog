<script setup>
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Dashboard</h1>
    </div>
    
    <div class="grid">
      <div class="card">
        <h3>Welcome</h3>
        <p>Welcome to the admin dashboard. Use the sidebar to navigate.</p>
      </div>
      <!-- Add more stats cards here later -->
    </div>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: 2rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

h3 {
  margin-bottom: 0.5rem;
}

p {
  color: var(--text-muted);
}
</style>
