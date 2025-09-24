<template>
  <div class="login-card">
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="login-email" class="form-label">Email</label>
        <input
          id="login-email"
          v-model="formData.email"
          type="email"
          class="form-input"
          :class="{ 'form-input--error': errors.email }"
          placeholder="Enter your email"
          required
          autocomplete="email"
          @blur="validateEmail"
        />
        <div v-if="errors.email" class="form-error">{{ errors.email }}</div>
      </div>

      <div class="form-group">
        <label for="login-password" class="form-label">Password</label>
        <div class="password-input-wrapper">
          <input
            id="login-password"
            v-model="formData.password"
            :type="showPassword ? 'text' : 'password'"
            class="form-input"
            :class="{ 'form-input--error': errors.password }"
            placeholder="Enter your password"
            required
            autocomplete="current-password"
            @blur="validatePassword"
          />
          <button
            type="button"
            class="password-toggle"
            @click="togglePasswordVisibility"
            :aria-label="showPassword ? 'Hide password' : 'Show password'"
          >
            <svg v-if="!showPassword" class="password-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            <svg v-else class="password-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
            </svg>
          </button>
        </div>
        <div v-if="errors.password" class="form-error">{{ errors.password }}</div>
      </div>

      <div class="form-actions">
        <button
          type="submit"
          class="btn btn--primary btn--full"
          :disabled="isLoading || !isFormValid"
        >
          <span v-if="isLoading" class="btn-spinner"></span>
          {{ isLoading ? 'Signing in...' : 'Sign in' }}
        </button>
      </div>

      <div class="form-footer">
        <p class="form-footer-text">
          Don't have an account?
          <button
            type="button"
            class="form-link"
            @click="switchToSignup"
          >
            Sign up
          </button>
        </p>
      </div>
    </form>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/modules/auth'
import { isValidEmail } from '@/utils/validation'

export default {
  name: 'LoginCard',
  emits: ['login', 'switch-to-signup'],
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      errors: {
        email: '',
        password: ''
      },
      showPassword: false,
      isLoading: false
    }
  },
  computed: {
    isFormValid() {
      return this.formData.email && 
             this.formData.password && 
             !this.errors.email && 
             !this.errors.password
    }
  },
  methods: {
    validateEmail() {
      if (!this.formData.email) {
        this.errors.email = 'Email is required'
        return false
      }
      if (!isValidEmail(this.formData.email)) {
        this.errors.email = 'Please enter a valid email address'
        return false
      }
      this.errors.email = ''
      return true
    },
    
    validatePassword() {
      if (!this.formData.password) {
        this.errors.password = 'Password is required'
        return false
      }
      if (this.formData.password.length < 6) {
        this.errors.password = 'Password must be at least 6 characters'
        return false
      }
      this.errors.password = ''
      return true
    },
    
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword
    },
    
    async handleLogin() {
      // Validate all fields
      const emailValid = this.validateEmail()
      const passwordValid = this.validatePassword()
      
      if (!emailValid || !passwordValid) {
        return
      }
      
      this.isLoading = true
      
      try {
        const authStore = useAuthStore()
        const userData = await authStore.mockLogin(this.formData.email, this.formData.password)
        
        console.log('LoginCard: Login successful', userData)
        this.$emit('login', userData)
        
        // Reset form
        this.formData = { email: '', password: '' }
        this.errors = { email: '', password: '' }
        
      } catch (error) {
        console.error('LoginCard: Login failed', error)
        
        // Handle specific error cases
        if (error.message.includes('User not found')) {
          this.errors.email = 'No account found with this email'
        } else if (error.message.includes('Invalid password')) {
          this.errors.password = 'Incorrect password'
        } else {
          this.errors.password = 'Login failed. Please try again.'
        }
      } finally {
        this.isLoading = false
      }
    },
    
    switchToSignup() {
      this.$emit('switch-to-signup')
    }
  }
}
</script>

<style scoped>
.login-card {
  width: 100%;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-primary, #1f2937);
  margin: 0;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--color-border, #e5e7eb);
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: var(--color-background, #ffffff);
  color: var(--color-text-primary, #1f2937);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input--error {
  border-color: var(--color-error, #ef4444);
}

.form-input--error:focus {
  border-color: var(--color-error, #ef4444);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: var(--color-text-secondary, #6b7280);
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: var(--color-text-primary, #1f2937);
}

.password-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.form-error {
  font-size: 0.875rem;
  color: var(--color-error, #ef4444);
  margin: 0;
}

.form-actions {
  margin-top: 0.5rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.btn--primary {
  background: var(--gradient-primary);
  color: white;
  box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.25);
}

.btn--primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px 0 rgba(59, 130, 246, 0.35);
}

.btn--primary:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px 0 rgba(59, 130, 246, 0.25);
}

.btn--full {
  width: 100%;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.btn-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.form-footer {
  text-align: center;
  margin-top: 1rem;
}

.form-footer-text {
  font-size: 0.875rem;
  color: var(--color-text-secondary, #6b7280);
  margin: 0;
}

.form-link {
  background: none;
  border: none;
  color: var(--color-primary);
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s ease;
}

.form-link:hover {
  color: var(--color-primary-dark);
}

/* Responsive design */
@media (max-width: 640px) {
  .login-form {
    gap: 1.25rem;
  }
  
  .form-input {
    padding: 0.625rem 0.875rem;
    font-size: 0.875rem;
  }
  
  .btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }
}
</style>
