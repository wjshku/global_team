<template>
  <nav class="app-navigation" v-if="isLoggedIn">
    <div class="nav-container">
      <ul class="nav-list">
        <li class="nav-item">
          <router-link to="/" class="nav-link" :class="{ active: $route.name === 'home' }">
            <span class="nav-icon">🏠</span>
            Home
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/personal" class="nav-link" :class="{ active: $route.name === 'personal' }">
            <span class="nav-icon">👤</span>
            Personal
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/teams" class="nav-link" :class="{ active: $route.name === 'teams' }">
            <span class="nav-icon">👥</span>
            Teams
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/meetings" class="nav-link" :class="{ active: $route.name === 'meetings' }">
            <span class="nav-icon">📅</span>
            Meetings
          </router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store/modules/auth'

const authStore = useAuthStore()
const isLoggedIn = computed(() => authStore.isLoggedIn)
</script>

<style scoped>
.app-navigation {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 0;
}

.nav-item {
  margin: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  text-decoration: none;
  color: #64748b;
  font-weight: 500;
  transition: all 0.2s ease;
  border-bottom: 3px solid transparent;
}

.nav-link:hover {
  color: #667eea;
  background: #f8fafc;
}

.nav-link.active {
  color: #667eea;
  border-bottom-color: #667eea;
  background: #f8fafc;
}

.nav-icon {
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .nav-list {
    flex-wrap: wrap;
  }
  
  .nav-link {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
}
</style>
