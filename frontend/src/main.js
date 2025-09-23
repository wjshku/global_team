import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './store/modules/auth'
import { useUIStore } from './store/modules/ui'
import './styles/variables.css'
import './styles/main.css'
import './styles/components.css'

const app = createApp(App)

// Use Pinia for state management
const pinia = createPinia()
app.use(pinia)

// Initialize stores
const authStore = useAuthStore()
authStore.initializeAuth()
const uiStore = useUIStore()
uiStore.initializeTheme()

// Use Vue Router
app.use(router)

// Mount the app
router.isReady().then(() => app.mount('#app'))