<template>
  <div class="not-found-view">
    <div class="not-found-content">
      <h1 class="not-found-title">404</h1>
      <h2 class="not-found-subtitle">Page Not Found</h2>
      <p class="not-found-message">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <div class="not-found-actions">
        <router-link to="/" class="home-link">
          Go Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style scoped>
.not-found-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}

.not-found-title {
  font-size: 6rem;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0 0 1rem 0;
  line-height: 1;
}

.not-found-subtitle {
  font-size: 2rem;
  font-weight: 600;
  color: var(--color-text-primary, #1f2937);
  margin: 0 0 1rem 0;
}

.not-found-message {
  font-size: 1.1rem;
  color: var(--color-text-secondary, #6b7280);
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.not-found-actions {
  margin-top: 2rem;
}

.home-link {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.home-link:hover {
  background: var(--color-primary-dark);
}

@media (max-width: 640px) {
  .not-found-title {
    font-size: 4rem;
  }
  
  .not-found-subtitle {
    font-size: 1.5rem;
  }
}
</style>