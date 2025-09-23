<template>
  <div class="signup-view">
    <div class="signup-container">
      <h1 class="signup-title">Create Account</h1>
      <p class="signup-description">
        Join the Global Team Manager to coordinate with your distributed team.
      </p>
      
      <div class="signup-form-container">
        <SignupCard @signup-success="handleSignupSuccess" />
      </div>
      
      <div class="signup-footer">
        <p class="signup-login-text">
          Already have an account? 
          <router-link to="/" class="login-link">Sign in here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import SignupCard from '@/components/features/SignupCard.vue'

export default {
  name: 'SignupView',
  components: {
    SignupCard
  },
  methods: {
    handleSignupSuccess(userData) {
      console.log('SignupView: Signup successful', userData)
      // Redirect to home page after successful signup
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.signup-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.signup-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  padding: 3rem;
  max-width: 500px;
  width: 100%;
}

.signup-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-text-primary, #1f2937);
  text-align: center;
  margin: 0 0 1rem 0;
}

.signup-description {
  font-size: 1.1rem;
  color: var(--color-text-secondary, #6b7280);
  text-align: center;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.signup-form-container {
  margin-bottom: 2rem;
}

.signup-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border, #e5e7eb);
}

.signup-login-text {
  font-size: 0.95rem;
  color: var(--color-text-secondary, #6b7280);
  margin: 0;
}

.login-link {
  color: var(--color-primary, #3b82f6);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.login-link:hover {
  color: var(--color-primary-dark, #2563eb);
  text-decoration: underline;
}

@media (max-width: 640px) {
  .signup-container {
    padding: 2rem;
    margin: 1rem;
  }
  
  .signup-title {
    font-size: 2rem;
  }
  
  .signup-description {
    font-size: 1rem;
  }
}
</style>
