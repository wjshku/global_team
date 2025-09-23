<!-- LoginCard.vue - Component for user login -->
<template>
  <BaseCard 
    title="Sign In" 
    class="login-card"
    :class="{ 'login-card--loading': loading }"
  >
    <BaseForm
      :model-value="formData"
      :rules="validationRules"
      :disabled="disabled"
      :loading="loading"
      submit-text="Sign In"
      @submit="handleSubmit"
    >
      <template #default="{ formData, errors }">
        <!-- Email Field -->
        <div class="form-field">
          <label for="login-email" class="form-label">Email Address</label>
          <input
            id="login-email"
            v-model="formData.email"
            type="email"
            class="form-input"
            :class="{ 'form-input--error': errors.email }"
            placeholder="Enter your email"
            :disabled="disabled || loading"
            @blur="validateField('email')"
          />
          <div v-if="errors.email" class="form-error">
            {{ errors.email }}
          </div>
        </div>

        <!-- Password Field -->
        <div class="form-field">
          <label for="login-password" class="form-label">Password</label>
          <input
            id="login-password"
            v-model="formData.password"
            type="password"
            class="form-input"
            :class="{ 'form-input--error': errors.password }"
            placeholder="Enter your password"
            :disabled="disabled || loading"
            @blur="validateField('password')"
          />
          <div v-if="errors.password" class="form-error">
            {{ errors.password }}
          </div>
        </div>

        <!-- Remember Me -->
        <div class="form-field form-field--checkbox">
          <label class="checkbox-label">
            <input
              v-model="formData.rememberMe"
              type="checkbox"
              class="checkbox-input"
              :disabled="disabled || loading"
            />
            <span class="checkbox-text">Remember me</span>
          </label>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="form-error-message">
          {{ errorMessage }}
        </div>
      </template>
    </BaseForm>

    <!-- Footer Actions -->
    <template #footer>
      <div class="login-card__footer">
        <BaseButton
          variant="secondary"
          size="small"
          @click="$emit('switch-to-signup')"
          :disabled="disabled || loading"
        >
          Don't have an account? Sign up
        </BaseButton>
      </div>
    </template>
  </BaseCard>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseForm from '@/components/common/BaseForm.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { isValidEmail } from '@/utils/validation'
import { VALIDATION_RULES, ERROR_MESSAGES } from '@/utils/constants'

// Props definition
const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  initialEmail: {
    type: String,
    default: ''
  }
})

// Emits definition
const emit = defineEmits(['login', 'switch-to-signup', 'error'])

// Store
const authStore = useAuthStore()

// Form data
const formData = reactive({
  email: props.initialEmail,
  password: '',
  rememberMe: false
})

// Error state
const errorMessage = ref('')

// Validation rules using utility functions
const validationRules = {
  email: [
    { required: true, message: 'Email is required' },
    { 
      validator: (value) => isValidEmail(value) || 'Please enter a valid email address'
    }
  ],
  password: [
    { required: true, message: 'Password is required' },
    { min: VALIDATION_RULES.PASSWORD.MIN_LENGTH, message: `Password must be at least ${VALIDATION_RULES.PASSWORD.MIN_LENGTH} characters` }
  ]
}

// Methods
const validateField = (fieldName) => {
  console.log(`LoginCard: Validating field ${fieldName}`)
  // Validation is handled by BaseForm
}

const handleSubmit = async ({ formData: data, event }) => {
  console.log('LoginCard: Form submitted', data)
  
  try {
    errorMessage.value = ''
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Use mock login with validation
    const userData = await authStore.mockLogin(data.email, data.password)
    
    console.log('LoginCard: Login successful', userData)
    emit('login', userData)
    
  } catch (error) {
    console.error('LoginCard: Login failed', error)
    errorMessage.value = error.message || ERROR_MESSAGES.UNAUTHORIZED
    emit('error', error)
  }
}

// Computed properties
const isFormValid = computed(() => {
  return formData.email && formData.password && 
         isValidEmail(formData.email) && 
         formData.password.length >= VALIDATION_RULES.PASSWORD.MIN_LENGTH
})
</script>

<style scoped>
.login-card {
  max-width: 400px;
  margin: 0 auto;
}

.login-card--loading {
  opacity: 0.8;
}

.form-field {
  margin-bottom: 1.5rem;
}

.form-field--checkbox {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--border-primary);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input--error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.checkbox-input {
  margin-right: 0.5rem;
  width: 1rem;
  height: 1rem;
}

.checkbox-text {
  user-select: none;
}

.form-error {
  color: #ef4444;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.form-error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.login-card__footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

/* Responsive design */
@media (max-width: 480px) {
  .login-card {
    margin: 0 1rem;
  }
  
  .form-input {
    padding: 0.6rem;
  }
}
</style>
