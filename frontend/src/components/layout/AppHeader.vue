<template>
  <header class="app-header">
    <div class="header-container">
      <div class="header-brand">
        <h1 class="brand-title">
          <span class="brand-icon">🌍</span>
          Global Team Manager
        </h1>
      </div>
      
      <div class="header-actions">
        <button @click="toggleTheme" class="theme-btn" :title="isDark ? 'Switch to light' : 'Switch to dark'">
          <span v-if="isDark">🌙</span>
          <span v-else>☀️</span>
        </button>

        <template v-if="isLoggedIn">
          <span class="welcome-text">Welcome, {{ currentUser?.name || 'User' }}</span>
          <button @click="handleLogout" class="logout-btn">
            Logout
          </button>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import { useUIStore } from '@/store/modules/ui'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const uiStore = useUIStore()
const router = useRouter()

const isLoggedIn = computed(() => authStore.isLoggedIn)
const currentUser = computed(() => authStore.currentUser)

const isDark = computed(() => uiStore.isDark)
const toggleTheme = () => uiStore.toggleTheme()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.brand-icon {
  font-size: 1.8rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.theme-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  transition: all 0.2s ease;
}

.theme-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.welcome-text {
  font-size: 0.9rem;
  opacity: 0.9;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .brand-title {
    font-size: 1.3rem;
  }
}
</style>
