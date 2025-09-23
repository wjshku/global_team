<template>
  <Teleport to="body">
    <Transition
      name="modal"
      @before-enter="handleBeforeEnter"
      @enter="handleEnter"
      @before-leave="handleBeforeLeave"
      @leave="handleLeave"
    >
      <div
        v-if="visible"
        class="base-modal-overlay"
        @click="handleOverlayClick"
      >
        <div
          :class="modalClasses"
          @click.stop
          role="dialog"
          :aria-modal="true"
          :aria-labelledby="titleId"
        >
          <!-- Modal Header -->
          <div v-if="$slots.header || title" class="base-modal__header">
            <slot name="header">
              <h2 :id="titleId" class="base-modal__title">{{ title }}</h2>
            </slot>
            <button
              v-if="closable"
              class="base-modal__close"
              @click="handleClose"
              aria-label="Close modal"
            >
              <svg class="modal-close-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Modal Body -->
          <div class="base-modal__body">
            <slot />
          </div>

          <!-- Modal Footer -->
          <div v-if="$slots.footer" class="base-modal__footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, ref, watch, nextTick } from 'vue'

// Props definition
const props = defineProps({
  // Modal visibility
  visible: {
    type: Boolean,
    default: false
  },
  // Modal title
  title: {
    type: String,
    default: ''
  },
  // Modal size
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'full'].includes(value)
  },
  // Close behavior
  closable: {
    type: Boolean,
    default: true
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  },
  closeOnEscape: {
    type: Boolean,
    default: true
  },
  // Animation
  animation: {
    type: String,
    default: 'fade',
    validator: (value) => ['fade', 'slide', 'scale'].includes(value)
  },
  // Additional CSS classes
  class: {
    type: String,
    default: ''
  }
})

// Emits definition
const emit = defineEmits(['update:visible', 'close', 'open'])

// Generate unique ID for accessibility
const titleId = ref(`modal-title-${Math.random().toString(36).substr(2, 9)}`)

// Computed classes for modal styling
const modalClasses = computed(() => {
  const baseClasses = 'base-modal'
  const sizeClass = `base-modal--${props.size}`
  const animationClass = `base-modal--${props.animation}`
  
  return [
    baseClasses,
    sizeClass,
    animationClass,
    props.class
  ].filter(Boolean).join(' ')
})

// Event handlers
const handleClose = () => {
  console.log('BaseModal close triggered:', {
    title: props.title,
    size: props.size,
    timestamp: new Date().toISOString()
  })
  
  emit('close')
  emit('update:visible', false)
}

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    console.log('BaseModal overlay clicked - closing modal')
    handleClose()
  }
}

// Keyboard event handler
const handleKeydown = (event) => {
  if (event.key === 'Escape' && props.closeOnEscape && props.visible) {
    console.log('BaseModal escape key pressed - closing modal')
    handleClose()
  }
}

// Animation handlers
const handleBeforeEnter = (el) => {
  console.log('BaseModal before enter animation')
  el.style.opacity = '0'
  if (props.animation === 'slide') {
    el.style.transform = 'translateY(-50px)'
  } else if (props.animation === 'scale') {
    el.style.transform = 'scale(0.8)'
  }
}

const handleEnter = (el, done) => {
  console.log('BaseModal enter animation')
  nextTick(() => {
    el.style.transition = 'all 0.3s ease-out'
    el.style.opacity = '1'
    if (props.animation === 'slide') {
      el.style.transform = 'translateY(0)'
    } else if (props.animation === 'scale') {
      el.style.transform = 'scale(1)'
    }
    setTimeout(done, 300)
  })
}

const handleBeforeLeave = (el) => {
  console.log('BaseModal before leave animation')
  el.style.transition = 'all 0.3s ease-in'
  el.style.opacity = '0'
  if (props.animation === 'slide') {
    el.style.transform = 'translateY(-50px)'
  } else if (props.animation === 'scale') {
    el.style.transform = 'scale(0.8)'
  }
}

const handleLeave = (el, done) => {
  console.log('BaseModal leave animation')
  setTimeout(done, 300)
}

// Watch for visibility changes
watch(() => props.visible, (newVisible) => {
  if (newVisible) {
    console.log('BaseModal opened:', {
      title: props.title,
      size: props.size,
      timestamp: new Date().toISOString()
    })
    emit('open')
    // Add keyboard event listener
    document.addEventListener('keydown', handleKeydown)
  } else {
    // Remove keyboard event listener
    document.removeEventListener('keydown', handleKeydown)
  }
})

// Cleanup on unmount
import { onUnmounted } from 'vue'
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Modal overlay */
.base-modal-overlay {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
}

/* Modal container */
.base-modal {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  max-height: 90vh;
  overflow: hidden;
  position: relative;
  max-width: 90vw;
}

/* Size variants */
.base-modal--small {
  width: 100%;
  max-width: 28rem;
}

.base-modal--medium {
  width: 100%;
  max-width: 32rem;
}

.base-modal--large {
  width: 100%;
  max-width: 42rem;
}

.base-modal--full {
  width: 100%;
  max-width: 56rem;
}

/* Modal sections */
.base-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.base-modal__title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.base-modal__close {
  padding: 0.5rem;
  color: #9ca3af;
  border-radius: 50%;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  background: none;
}

.base-modal__close:hover {
  color: #4b5563;
  background-color: #f3f4f6;
}

.modal-close-icon {
  width: 1.5rem;
  height: 1.5rem;
}

.base-modal__body {
  padding: 1.5rem;
  overflow-y: auto;
  max-height: calc(90vh - 120px);
}

.base-modal__footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
  background-color: #f9fafb;
}

/* Animation variants */
.base-modal--fade {
  transition: opacity 0.3s ease;
}

.base-modal--slide {
  transition: all 0.3s ease;
}

.base-modal--scale {
  transition: all 0.3s ease;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .base-modal {
    background-color: #1f2937;
    color: white;
  }
  
  .base-modal__header {
    border-color: #374151;
  }
  
  .base-modal__footer {
    border-color: #374151;
    background-color: #111827;
  }
  
  .base-modal__title {
    color: white;
  }
  
  .base-modal__close {
    color: #9ca3af;
  }
  
  .base-modal__close:hover {
    color: #e5e7eb;
    background-color: #374151;
  }
}

/* Responsive design */
@media (max-width: 640px) {
  .base-modal {
    margin: 1rem;
    max-width: calc(100vw - 2rem);
  }
  
  .base-modal__header,
  .base-modal__body,
  .base-modal__footer {
    padding: 1rem;
  }
  
  .base-modal__body {
    max-height: calc(90vh - 100px);
  }
}

/* Focus management */
.base-modal:focus {
  outline: none;
}

/* Accessibility improvements */
.base-modal[aria-hidden="true"] {
  display: none;
}
</style>
