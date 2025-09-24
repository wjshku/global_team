<template>
  <div class="signup-card">
    <form @submit.prevent="handleSignup" class="signup-form">
      <div class="form-group">
        <label for="signup-name" class="form-label">Full Name</label>
        <input
          id="signup-name"
          v-model="formData.name"
          type="text"
          class="form-input"
          :class="{ 'form-input--error': errors.name }"
          placeholder="Enter your full name"
          required
          autocomplete="name"
          @blur="validateName"
        />
        <div v-if="errors.name" class="form-error">{{ errors.name }}</div>
      </div>

      <div class="form-group">
        <label for="signup-email" class="form-label">Email</label>
        <input
          id="signup-email"
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
        <label for="signup-password" class="form-label">Password</label>
        <div class="password-input-wrapper">
          <input
            id="signup-password"
            v-model="formData.password"
            :type="showPassword ? 'text' : 'password'"
            class="form-input"
            :class="{ 'form-input--error': errors.password }"
            placeholder="Create a password"
            required
            autocomplete="new-password"
            @blur="validatePassword"
            @input="validatePassword"
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
        <div v-if="passwordStrength.show" class="password-strength">
          <div class="password-strength-bar">
            <div 
              class="password-strength-fill" 
              :class="passwordStrength.level"
              :style="{ width: passwordStrength.percentage + '%' }"
            ></div>
          </div>
          <div class="password-strength-text">{{ passwordStrength.text }}</div>
        </div>
      </div>

      <div class="form-group">
        <label for="signup-timezone" class="form-label">Timezone</label>
        <select
          id="signup-timezone"
          v-model="formData.timezone"
          class="form-select"
          :class="{ 'form-select--error': errors.timezone }"
          required
          @blur="validateTimezone"
        >
          <option value="" disabled>Select your timezone</option>
          <option 
            v-for="tz in timezones" 
            :key="tz.tz" 
            :value="tz.tz"
          >
            {{ formatTimezoneLabel(tz) }}
          </option>
        </select>
        <div v-if="errors.timezone" class="form-error">{{ errors.timezone }}</div>
      </div>

      <div class="form-group">
        <label class="checkbox-wrapper">
          <input
            v-model="formData.agreeToTerms"
            type="checkbox"
            class="checkbox-input"
            required
          />
          <span class="checkbox-label">
            I agree to the 
            <a href="#" class="terms-link" @click.prevent="showTerms">Terms of Service</a>
            and 
            <a href="#" class="terms-link" @click.prevent="showPrivacy">Privacy Policy</a>
          </span>
        </label>
        <div v-if="errors.agreeToTerms" class="form-error">{{ errors.agreeToTerms }}</div>
      </div>

      <div class="form-actions">
        <button
          type="submit"
          class="btn btn--primary btn--full"
          :disabled="isLoading || !isFormValid"
        >
          <span v-if="isLoading" class="btn-spinner"></span>
          {{ isLoading ? 'Creating account...' : 'Create account' }}
        </button>
      </div>

      <div class="form-footer">
        <p class="form-footer-text">
          Already have an account?
          <button
            type="button"
            class="form-link"
            @click="switchToLogin"
          >
            Sign in
          </button>
        </p>
      </div>
    </form>
  </div>
</template>

<script>
import { useAuthStore } from '@/store/modules/auth'
import { isValidEmail, validatePassword } from '@/utils/validation'
import { getUnifiedTimezones, formatTimezoneCurrentLabel } from '@/utils/timezone'

export default {
  name: 'SignupCard',
  emits: ['signup', 'switch-to-login'],
  data() {
    return {
      formData: {
        name: '',
        email: '',
        password: '',
        timezone: '',
        agreeToTerms: false
      },
      errors: {
        name: '',
        email: '',
        password: '',
        timezone: '',
        agreeToTerms: ''
      },
      showPassword: false,
      isLoading: false,
      timezones: getUnifiedTimezones()
    }
  },
  computed: {
    isFormValid() {
      return this.formData.name && 
             this.formData.email && 
             this.formData.password && 
             this.formData.timezone &&
             this.formData.agreeToTerms &&
             !this.errors.name && 
             !this.errors.email && 
             !this.errors.password && 
             !this.errors.timezone &&
             !this.errors.agreeToTerms
    },
    
    passwordStrength() {
      if (!this.formData.password) {
        return { show: false }
      }
      
      const validation = validatePassword(this.formData.password)
      const length = this.formData.password.length
      
      if (length < 6) {
        return {
          show: true,
          level: 'weak',
          percentage: 25,
          text: 'Too short'
        }
      } else if (length < 8) {
        return {
          show: true,
          level: 'fair',
          percentage: 50,
          text: 'Fair'
        }
      } else if (validation.isValid) {
        return {
          show: true,
          level: 'strong',
          percentage: 100,
          text: 'Strong'
        }
      } else {
        return {
          show: true,
          level: 'fair',
          percentage: 75,
          text: 'Good'
        }
      }
    }
  },
  mounted() {
    // Set default timezone to user's current timezone
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone
    if (this.timezones.find(tz => tz.tz === userTimezone)) {
      this.formData.timezone = userTimezone
    }
  },
  methods: {
    validateName() {
      if (!this.formData.name) {
        this.errors.name = 'Name is required'
        return false
      }
      if (this.formData.name.trim().length < 2) {
        this.errors.name = 'Name must be at least 2 characters'
        return false
      }
      this.errors.name = ''
      return true
    },
    
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
      
      const validation = validatePassword(this.formData.password)
      if (!validation.isValid) {
        this.errors.password = validation.message
        return false
      }
      
      this.errors.password = ''
      return true
    },
    
    validateTimezone() {
      if (!this.formData.timezone) {
        this.errors.timezone = 'Timezone is required'
        return false
      }
      this.errors.timezone = ''
      return true
    },
    
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword
    },
    
    formatTimezoneLabel(timezone) {
      return formatTimezoneCurrentLabel(timezone.tz)
    },
    
    showTerms() {
      // TODO: Implement terms modal or navigation
      console.log('Show terms of service')
    },
    
    showPrivacy() {
      // TODO: Implement privacy policy modal or navigation
      console.log('Show privacy policy')
    },
    
    async handleSignup() {
      // Validate all fields
      const nameValid = this.validateName()
      const emailValid = this.validateEmail()
      const passwordValid = this.validatePassword()
      const timezoneValid = this.validateTimezone()
      
      if (!this.formData.agreeToTerms) {
        this.errors.agreeToTerms = 'You must agree to the terms and conditions'
        return
      }
      
      if (!nameValid || !emailValid || !passwordValid || !timezoneValid) {
        return
      }
      
      this.isLoading = true
      
      try {
        const authStore = useAuthStore()
        const userData = await authStore.mockSignup({
          name: this.formData.name.trim(),
          email: this.formData.email.trim(),
          password: this.formData.password,
          timezone: this.formData.timezone
        })
        
        console.log('SignupCard: Signup successful', userData)
        this.$emit('signup', userData)
        
        // Reset form
        this.formData = {
          name: '',
          email: '',
          password: '',
          timezone: '',
          agreeToTerms: false
        }
        this.errors = {
          name: '',
          email: '',
          password: '',
          timezone: '',
          agreeToTerms: ''
        }
        
      } catch (error) {
        console.error('SignupCard: Signup failed', error)
        
        // Handle specific error cases
        if (error.message.includes('User already exists')) {
          this.errors.email = 'An account with this email already exists'
        } else {
          this.errors.email = 'Signup failed. Please try again.'
        }
      } finally {
        this.isLoading = false
      }
    },
    
    switchToLogin() {
      this.$emit('switch-to-login')
    }
  }
}
</script>

<style scoped>
.signup-card {
  width: 100%;
}

.signup-form {
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

.form-input,
.form-select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--color-border, #e5e7eb);
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: var(--color-background, #ffffff);
  color: var(--color-text-primary, #1f2937);
}

.form-select {
  cursor: pointer;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-primary, #3b82f6);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input--error,
.form-select--error {
  border-color: var(--color-error, #ef4444);
}

.form-input--error:focus,
.form-select--error:focus {
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

.password-strength {
  margin-top: 0.5rem;
}

.password-strength-bar {
  width: 100%;
  height: 4px;
  background: var(--color-border, #e5e7eb);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.password-strength-fill {
  height: 100%;
  transition: all 0.3s ease;
}

.password-strength-fill.weak {
  background: var(--color-error, #ef4444);
}

.password-strength-fill.fair {
  background: var(--color-warning, #f59e0b);
}

.password-strength-fill.strong {
  background: var(--color-success, #10b981);
}

.password-strength-text {
  font-size: 0.75rem;
  color: var(--color-text-secondary, #6b7280);
  text-align: right;
}

.checkbox-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
}

.checkbox-input {
  margin: 0;
  width: 1rem;
  height: 1rem;
  accent-color: var(--color-primary, #3b82f6);
}

.checkbox-label {
  font-size: 0.875rem;
  color: var(--color-text-secondary, #6b7280);
  line-height: 1.5;
}

.terms-link {
  color: var(--color-primary, #3b82f6);
  text-decoration: underline;
  transition: color 0.2s ease;
}

.terms-link:hover {
  color: var(--color-primary-dark, #1d4ed8);
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
  background: linear-gradient(135deg, var(--color-primary, #3b82f6) 0%, var(--color-primary-dark, #1d4ed8) 100%);
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
  color: var(--color-primary, #3b82f6);
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s ease;
}

.form-link:hover {
  color: var(--color-primary-dark, #1d4ed8);
}

/* Responsive design */
@media (max-width: 640px) {
  .signup-form {
    gap: 1.25rem;
  }
  
  .form-input,
  .form-select {
    padding: 0.625rem 0.875rem;
    font-size: 0.875rem;
  }
  
  .btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }
  
  .checkbox-wrapper {
    gap: 0.5rem;
  }
  
  .checkbox-label {
    font-size: 0.8125rem;
  }
}
</style>
