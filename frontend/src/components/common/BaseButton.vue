<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
    :type="type"
  >
    <!-- Loading spinner -->
    <div v-if="loading" class="loading-spinner" />
    
    <!-- Button content -->
    <span :class="{ 'button-content--hidden': loading }">
      <slot />
    </span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

// Props definition
const props = defineProps({
  // Button style variants
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger'].includes(value)
  },
  // Button sizes
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  // Button states
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  // HTML button type
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },
  // Additional CSS classes
  class: {
    type: String,
    default: ''
  }
})

// Emits definition
const emit = defineEmits(['click'])

// Computed classes for button styling
const buttonClasses = computed(() => {
  const baseClasses = 'base-button'
  const variantClass = `base-button--${props.variant}`
  const sizeClass = `base-button--${props.size}`
  const stateClass = props.disabled ? 'base-button--disabled' : ''
  const loadingClass = props.loading ? 'base-button--loading' : ''
  
  return [
    baseClasses,
    variantClass,
    sizeClass,
    stateClass,
    loadingClass,
    props.class
  ].filter(Boolean).join(' ')
})

// Click handler with debugging
const handleClick = (event) => {
  console.log('BaseButton clicked:', {
    variant: props.variant,
    size: props.size,
    disabled: props.disabled,
    loading: props.loading,
    type: props.type,
    timestamp: new Date().toISOString()
  })
  
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.base-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  position: relative;
  cursor: pointer;
  border: none;
  outline: none;
  font-family: inherit;
}

.base-button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

/* Variant styles */
.base-button--primary {
  background-color: #2563eb;
  color: white;
}

.base-button--primary:hover {
  background-color: #1d4ed8;
}

.base-button--primary:focus {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

.base-button--secondary {
  background-color: #e5e7eb;
  color: #111827;
}

.base-button--secondary:hover {
  background-color: #d1d5db;
}

.base-button--secondary:focus {
  box-shadow: 0 0 0 2px rgba(107, 114, 128, 0.5);
}

.base-button--danger {
  background-color: #dc2626;
  color: white;
}

.base-button--danger:hover {
  background-color: #b91c1c;
}

.base-button--danger:focus {
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.5);
}

/* Size styles */
.base-button--small {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.base-button--medium {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.base-button--large {
  padding: 0.75rem 1.5rem;
  font-size: 1.125rem;
}

/* State styles */
.base-button--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.base-button--loading {
  cursor: wait;
}

/* Loading spinner */
.loading-spinner {
  position: absolute;
  width: 1rem;
  height: 1rem;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Hover effects */
.base-button:not(.base-button--disabled):not(.base-button--loading):hover {
  transform: scale(1.05);
}

/* Active state */
.base-button:not(.base-button--disabled):not(.base-button--loading):active {
  transform: scale(0.95);
}

/* Button content states */
.button-content--hidden {
  opacity: 0;
}
</style>
