<template>
  <div :class="cardClasses" @click="handleCardClick">
    <!-- Card Header -->
    <div v-if="$slots.header || title" class="base-card__header">
      <slot name="header">
        <h3 v-if="title" class="base-card__title">{{ title }}</h3>
      </slot>
    </div>

    <!-- Card Body -->
    <div class="base-card__body">
      <slot />
    </div>

    <!-- Card Footer -->
    <div v-if="$slots.footer" class="base-card__footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props definition
const props = defineProps({
  // Card title (optional, can be overridden by header slot)
  title: {
    type: String,
    default: ''
  },
  // Visual appearance options
  shadow: {
    type: Boolean,
    default: true
  },
  border: {
    type: Boolean,
    default: true
  },
  hover: {
    type: Boolean,
    default: true
  },
  // Card padding
  padding: {
    type: String,
    default: 'medium',
    validator: (value) => ['none', 'small', 'medium', 'large'].includes(value)
  },
  // Additional CSS classes
  class: {
    type: String,
    default: ''
  },
  // Clickable card
  clickable: {
    type: Boolean,
    default: false
  }
})

// Emits definition
const emit = defineEmits(['click'])

// Computed classes for card styling
const cardClasses = computed(() => {
  const baseClasses = 'base-card'
  const shadowClass = props.shadow ? 'base-card--shadow' : ''
  const borderClass = props.border ? 'base-card--border' : ''
  const hoverClass = props.hover ? 'base-card--hover' : ''
  const paddingClass = `base-card--padding-${props.padding}`
  const clickableClass = props.clickable ? 'base-card--clickable' : ''
  
  return [
    baseClasses,
    shadowClass,
    borderClass,
    hoverClass,
    paddingClass,
    clickableClass,
    props.class
  ].filter(Boolean).join(' ')
})

// Click handler with debugging
const handleCardClick = (event) => {
  if (props.clickable) {
    console.log('BaseCard clicked:', {
      title: props.title,
      clickable: props.clickable,
      timestamp: new Date().toISOString()
    })
    emit('click', event)
  }
}
</script>

<style scoped>
.base-card {
  background-color: var(--bg-primary);
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  position: relative;
}

/* Shadow variants */
.base-card--shadow {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.base-card--shadow:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Border variants */
.base-card--border {
  border: 1px solid var(--border-primary);
}

/* Hover effects */
.base-card--hover:hover {
  transform: translateY(-2px);
}

/* Clickable state */
.base-card--clickable {
  cursor: pointer;
}

.base-card--clickable:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Padding variants */
.base-card--padding-none {
  padding: 0;
}

.base-card--padding-small {
  padding: 0.75rem;
}

.base-card--padding-medium {
  padding: 1rem;
}

.base-card--padding-large {
  padding: 1.5rem;
}

/* Card sections */
.base-card__header {
  border-bottom: 1px solid var(--border-primary);
  padding-bottom: 0.75rem;
  margin-bottom: 1rem;
}

.base-card__title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.base-card__body {
  flex: 1;
}

.base-card__footer {
  border-top: 1px solid var(--border-primary);
  padding-top: 0.75rem;
  margin-top: 1rem;
}
</style>
