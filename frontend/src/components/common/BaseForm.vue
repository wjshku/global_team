<template>
  <form 
    :class="formClasses" 
    @submit="handleSubmit"
    @input="handleInput"
    @change="handleChange"
  >
    <!-- Form content slot -->
    <slot :formData="formData" :errors="errors" />
    
    <!-- Submit button (optional) -->
    <div v-if="showSubmitButton" class="base-form__actions">
      <BaseButton
        :type="submitButtonType"
        :variant="submitButtonVariant"
        :size="submitButtonSize"
        :disabled="disabled || loading"
        :loading="loading"
        @click="handleSubmitClick"
      >
        {{ submitText }}
      </BaseButton>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import BaseButton from './BaseButton.vue'
import { validateRequired } from '@/utils/validation'

// Props definition
const props = defineProps({
  // Form configuration
  modelValue: {
    type: Object,
    default: () => ({})
  },
  // Validation rules
  rules: {
    type: Object,
    default: () => ({})
  },
  // Form state
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  // Submit button configuration
  submitText: {
    type: String,
    default: 'Submit'
  },
  showSubmitButton: {
    type: Boolean,
    default: true
  },
  submitButtonType: {
    type: String,
    default: 'submit',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },
  submitButtonVariant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value)
  },
  submitButtonSize: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  // Form layout
  layout: {
    type: String,
    default: 'vertical',
    validator: (value) => ['vertical', 'horizontal', 'inline'].includes(value)
  },
  // Additional CSS classes
  class: {
    type: String,
    default: ''
  }
})

// Emits definition
const emit = defineEmits([
  'update:modelValue',
  'submit',
  'input',
  'change',
  'validate'
])

// Form data management
const formData = reactive({ ...props.modelValue })
const errors = reactive({})

// Computed classes for form styling
const formClasses = computed(() => {
  const baseClasses = 'base-form'
  const layoutClass = `base-form--${props.layout}`
  const disabledClass = props.disabled ? 'base-form--disabled' : ''
  const loadingClass = props.loading ? 'base-form--loading' : ''
  
  return [
    baseClasses,
    layoutClass,
    disabledClass,
    loadingClass,
    props.class
  ].filter(Boolean).join(' ')
})

// Watch for external modelValue changes
watch(() => props.modelValue, (newValue) => {
  Object.assign(formData, newValue)
}, { deep: true })

// Watch for formData changes and emit updates
watch(formData, (newValue) => {
  console.log('BaseForm data changed:', newValue)
  emit('update:modelValue', { ...newValue })
}, { deep: true })

// Validation function
const validateField = (fieldName, value) => {
  const rules = props.rules[fieldName]
  if (!rules) return true

  for (const rule of rules) {
    if (typeof rule === 'function') {
      const result = rule(value)
      if (result !== true) {
        return result
      }
    } else if (typeof rule === 'object') {
      if (rule.required && (!value || value.toString().trim() === '')) {
        return rule.message || `${fieldName} is required`
      }
      if (rule.min && value.length < rule.min) {
        return rule.message || `${fieldName} must be at least ${rule.min} characters`
      }
      if (rule.max && value.length > rule.max) {
        return rule.message || `${fieldName} must be no more than ${rule.max} characters`
      }
      if (rule.pattern && !rule.pattern.test(value)) {
        return rule.message || `${fieldName} format is invalid`
      }
    }
  }
  return true
}

// Validate entire form
const validateForm = () => {
  const newErrors = {}
  let isValid = true

  // First check required fields using utility function
  const requiredFields = Object.keys(props.rules).filter(fieldName => {
    const rules = props.rules[fieldName]
    return rules.some(rule => rule.required === true)
  })
  
  if (requiredFields.length > 0) {
    const requiredValidation = validateRequired(formData, requiredFields)
    if (!requiredValidation.isValid) {
      requiredValidation.missingFields.forEach(field => {
        newErrors[field] = `${field} is required`
      })
      isValid = false
    }
  }

  // Then validate individual fields
  for (const fieldName in props.rules) {
    const fieldValue = formData[fieldName]
    const error = validateField(fieldName, fieldValue)
    
    if (error !== true) {
      newErrors[fieldName] = error
      isValid = false
    }
  }

  // Update errors
  Object.keys(errors).forEach(key => delete errors[key])
  Object.assign(errors, newErrors)

  console.log('BaseForm validation:', { isValid, errors: newErrors })
  emit('validate', { isValid, errors: newErrors })
  
  return isValid
}

// Event handlers
const handleSubmit = (event) => {
  event.preventDefault()
  
  console.log('BaseForm submit triggered:', {
    formData: { ...formData },
    disabled: props.disabled,
    loading: props.loading,
    timestamp: new Date().toISOString()
  })

  if (props.disabled || props.loading) {
    return
  }

  const isValid = validateForm()
  if (isValid) {
    emit('submit', { formData: { ...formData }, event })
  }
}

const handleSubmitClick = (event) => {
  console.log('BaseForm submit button clicked')
  handleSubmit(event)
}

const handleInput = (event) => {
  console.log('BaseForm input event:', event.target.name, event.target.value)
  emit('input', { event, formData: { ...formData } })
}

const handleChange = (event) => {
  console.log('BaseForm change event:', event.target.name, event.target.value)
  emit('change', { event, formData: { ...formData } })
}

// Expose methods for parent components
defineExpose({
  validateForm,
  formData,
  errors
})
</script>

<style scoped>
.base-form {
  width: 100%;
}

/* Layout variants */
.base-form--vertical {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.base-form--horizontal {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.base-form--inline {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 1rem;
}

/* State styles */
.base-form--disabled {
  opacity: 0.5;
  pointer-events: none;
}

.base-form--loading {
  pointer-events: none;
}

/* Form actions */
.base-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 1rem;
}

.base-form--inline .base-form__actions {
  padding-top: 0;
}

/* Error states */
.base-form :deep(.error) {
  border-color: #ef4444;
}

.base-form :deep(.error:focus) {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.base-form :deep(.error-message) {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Responsive design */
@media (max-width: 640px) {
  .base-form--horizontal {
    gap: 0.75rem;
  }
  
  .base-form--inline {
    flex-direction: column;
    align-items: stretch;
  }
  
  .base-form__actions {
    flex-direction: column;
  }
}
</style>
