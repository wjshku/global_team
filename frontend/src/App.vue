<template>
  <div id="app">
    <AppHeader />
    <AppNavigation />
    <main class="main-content view">
      <router-view />
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from './components/layout/AppHeader.vue'
import AppNavigation from './components/layout/AppNavigation.vue'
import AppFooter from './components/layout/AppFooter.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppNavigation,
    AppFooter
  },
  mounted() {
    // This proves the router is available in App.vue
    console.log('App.vue mounted - Router available:', this.$router)
    console.log('Current route:', this.$route)
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  background-color: var(--bg-secondary);
  color: var(--text-primary);
}

/* Global styles */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
  background-color: var(--bg-secondary);
}

/* Router transition styles */
.router-enter-active,
.router-leave-active {
  transition: opacity 0.3s ease;
}

.router-enter-from,
.router-leave-to {
  opacity: 0;
}
</style>
