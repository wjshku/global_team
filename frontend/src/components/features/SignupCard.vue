<!-- SignupCard.vue - Component for user registration -->
<template>
  <BaseCard 
    title="Create Account" 
    class="signup-card"
    :class="{ 'signup-card--loading': loading }"
  >
    <BaseForm
      :model-value="formData"
      :rules="validationRules"
      :disabled="disabled"
      :loading="loading"
      submit-text="Create Account"
      @submit="handleSubmit"
    >
      <template #default="{ formData, errors }">
        <!-- Name Field -->
        <div class="form-field">
          <label for="name" class="form-label">Full Name</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            class="form-input"
            :class="{ 'form-input--error': errors.name }"
            placeholder="Enter your full name"
            :disabled="disabled || loading"
            @blur="validateField('name')"
          />
          <div v-if="errors.name" class="form-error">
            {{ errors.name }}
          </div>
        </div>

        <!-- Email Field -->
        <div class="form-field">
          <label for="email" class="form-label">Email Address</label>
          <input
            id="email"
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
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            class="form-input"
            :class="{ 'form-input--error': errors.password }"
            placeholder="Create a password"
            :disabled="disabled || loading"
            @blur="validateField('password')"
          />
          <div v-if="errors.password" class="form-error">
            {{ errors.password }}
          </div>
        </div>

        <!-- Confirm Password Field -->
        <div class="form-field">
          <label for="confirmPassword" class="form-label">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="formData.confirmPassword"
            type="password"
            class="form-input"
            :class="{ 'form-input--error': errors.confirmPassword }"
            placeholder="Confirm your password"
            :disabled="disabled || loading"
            @blur="validateField('confirmPassword')"
          />
          <div v-if="errors.confirmPassword" class="form-error">
            {{ errors.confirmPassword }}
          </div>
        </div>

        <!-- Timezone Field -->
        <div class="form-field">
          <label for="timezone" class="form-label">Timezone</label>
          <select
            id="timezone"
            v-model="formData.timezone"
            class="form-select"
            :class="{ 'form-select--error': errors.timezone }"
            :disabled="disabled || loading"
            @blur="validateField('timezone')"
          >
            <option value="">Select your timezone</option>
            <option 
              v-for="tz in timezoneOptions" 
              :key="tz.value" 
              :value="tz.value"
            >
              {{ tz.label }}
            </option>
          </select>
          <div v-if="errors.timezone" class="form-error">
            {{ errors.timezone }}
          </div>
        </div>

        <!-- Terms and Conditions -->
        <div class="form-field form-field--checkbox">
          <label class="checkbox-label">
            <input
              v-model="formData.acceptTerms"
              type="checkbox"
              class="checkbox-input"
              :disabled="disabled || loading"
            />
            <span class="checkbox-text">
              I agree to the 
              <a href="#" class="link" @click.prevent="$emit('show-terms')">Terms of Service</a>
              and 
              <a href="#" class="link" @click.prevent="$emit('show-privacy')">Privacy Policy</a>
            </span>
          </label>
          <div v-if="errors.acceptTerms" class="form-error">
            {{ errors.acceptTerms }}
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="form-error-message">
          {{ errorMessage }}
        </div>
      </template>
    </BaseForm>

    <!-- Footer Actions -->
    <template #footer>
      <div class="signup-card__footer">
        <BaseButton
          variant="secondary"
          size="small"
          @click="$emit('switch-to-login')"
          :disabled="disabled || loading"
        >
          Already have an account? Sign in
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
import { isValidEmail, validatePassword, validateRequired } from '@/utils/validation'
import { getUnifiedTimezones, formatTimezoneCurrentLabel } from '@/utils/timezone'
import { VALIDATION_RULES, ERROR_MESSAGES, SUCCESS_MESSAGES } from '@/utils/constants'

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
const emit = defineEmits(['signup', 'switch-to-login', 'show-terms', 'show-privacy', 'error'])

// Store
const authStore = useAuthStore()

// Form data
const formData = reactive({
  name: '',
  email: props.initialEmail,
  password: '',
  confirmPassword: '',
  timezone: '',
  acceptTerms: false
})

// Error state
const errorMessage = ref('')

// Timezone options built from unified list with current labels
const timezoneOptions = getUnifiedTimezones().map(({ tz, city }) => ({
  value: tz,
  label: formatTimezoneCurrentLabel(tz)
}))

// Validation rules using utility functions
const validationRules = {
  name: [
    { required: true, message: 'Full name is required' },
    { min: VALIDATION_RULES.TEAM_NAME.MIN_LENGTH, message: `Name must be at least ${VALIDATION_RULES.TEAM_NAME.MIN_LENGTH} characters` }
  ],
  email: [
    { required: true, message: 'Email is required' },
    { 
      validator: (value) => isValidEmail(value) || 'Please enter a valid email address'
    }
  ],
  password: [
    { required: true, message: 'Password is required' },
    {
      validator: (value) => {
        const result = validatePassword(value)
        return result.isValid || result.message
      }
    }
  ],
  confirmPassword: [
    { required: true, message: 'Please confirm your password' },
    {
      validator: (value) => value === formData.password || 'Passwords do not match'
    }
  ],
  timezone: [
    { required: true, message: 'Please select your timezone' }
  ],
  acceptTerms: [
    {
      validator: (value) => value === true || 'You must accept the terms and conditions'
    }
  ]
}

// Methods
const validateField = (fieldName) => {
  console.log(`SignupCard: Validating field ${fieldName}`)
  // Validation is handled by BaseForm
}

const handleSubmit = async ({ formData: data, event }) => {
  console.log('SignupCard: Form submitted', data)
  
  try {
    errorMessage.value = ''
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Use mock signup with validation
    const userData = await authStore.mockSignup({
      name: data.name,
      email: data.email,
      password: data.password,
      timezone: data.timezone
    })
    
    console.log('SignupCard: Signup successful', userData)
    emit('signup', userData)
    
  } catch (error) {
    console.error('SignupCard: Signup failed', error)
    errorMessage.value = error.message || ERROR_MESSAGES.GENERIC
    emit('error', error)
  }
}

// Computed properties
const isFormValid = computed(() => {
  const requiredFields = ['name', 'email', 'password', 'confirmPassword', 'timezone']
  const requiredValidation = validateRequired(formData, requiredFields)
  
  return requiredValidation.isValid &&
         isValidEmail(formData.email) &&
         validatePassword(formData.password).isValid &&
         formData.password === formData.confirmPassword &&
         formData.acceptTerms
})
</script>

<style scoped>
.signup-card {
  max-width: 450px;
  margin: 0 auto;
}

.signup-card--loading {
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

.form-input,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--border-primary);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  background: white;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input--error,
.form-select--error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.4;
}

.checkbox-input {
  margin-right: 0.5rem;
  width: 1rem;
  height: 1rem;
  margin-top: 0.1rem;
  flex-shrink: 0;
}

.checkbox-text {
  user-select: none;
}

.link {
  color: var(--color-primary);
  text-decoration: underline;
  cursor: pointer;
}

.link:hover {
  color: var(--color-primary-dark);
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

.signup-card__footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

/* Responsive design */
@media (max-width: 480px) {
  .signup-card {
    margin: 0 1rem;
  }
  
  .form-input,
  .form-select {
    padding: 0.6rem;
  }
}
</style>
