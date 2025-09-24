<template>
  <div class="auth-view">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-card__content">
          <div class="auth-header">
            <h1 class="auth-title">Welcome back</h1>
            <p class="auth-description">Sign in to continue to {{ appName }}</p>
          </div>
          <div class="auth-form-container">
            <LoginCard 
              ref="loginCard"
              @login="handleLoginSuccess" 
              @switch-to-signup="goToSignup"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoginCard from '@/components/features/LoginCard.vue'
import { APP_NAME } from '@/utils/constants'
import { useAuthStore } from '@/store/modules/auth'

export default {
  name: 'LoginView',
  components: {
    LoginCard
  },
  data() {
    return {
      appName: APP_NAME
    }
  },
  async created() {
    // Check if user is already authenticated
    const authStore = useAuthStore()
    await authStore.initializeAuth()
    
    if (authStore.isLoggedIn) {
      console.log('LoginView: User already authenticated, redirecting to home')
      this.$router.push('/')
    }
  },
  methods: {
    handleLoginSuccess(userData) {
      console.log('LoginView: Login successful', userData)
      // Navigate to home page
      this.$router.push('/')
    },
    
    goToSignup() {
      this.$router.push('/signup')
    }
  }
}
</script>

<style scoped>
.auth-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #ffffff;
  position: relative;
  overflow: hidden;
}

.auth-container {
  max-width: 480px;
  width: 100%;
  position: relative;
  z-index: 1;
}

.auth-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 32px 64px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

.auth-card__content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 3rem;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--color-text-primary, #1f2937);
  margin: 0 0 0.75rem 0;
  letter-spacing: -0.025em;
  background: var(--gradient-secondary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-description {
  font-size: 1.1rem;
  color: var(--color-text-secondary, #6b7280);
  margin: 0;
  line-height: 1.6;
  font-weight: 400;
}

.auth-form-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Animation improvements */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-card__content {
  animation: fadeInUp 0.6s ease-out;
}

/* Focus states for accessibility */
.auth-card:focus-within {
  outline: 2px solid var(--color-primary);
  outline-offset: 4px;
}

/* Responsive design */
@media (max-width: 640px) {
  .auth-view {
    padding: 1rem;
  }
  
  .auth-container {
    max-width: 100%;
  }
  
  .auth-card__content {
    padding: 2rem 1.5rem;
  }
  
  .auth-title {
    font-size: 1.875rem;
  }
  
  .auth-description {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .auth-card__content {
    padding: 1.5rem 1rem;
  }
  
  .auth-title {
    font-size: 1.75rem;
  }
}
</style>
