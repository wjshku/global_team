<!-- TimezoneSelectorCard.vue - Reusable card component for timezone selection -->
<template>
  <BaseCard 
    :title="title"
    :class="cardClasses"
    :clickable="false"
  >
    <!-- Timezone Selection -->
    <div class="timezone-selector">
      <div class="timezone-field">
        <label for="timezone-select" class="timezone-label">
          {{ label }}
        </label>
        <select
          id="timezone-select"
          v-model="selectedTimezone"
          class="timezone-select"
          :class="{ 'timezone-select--error': hasError }"
          :disabled="disabled"
          @change="handleTimezoneChange"
        >
          <option value="" disabled>{{ placeholder }}</option>
          <option 
            v-for="timezone in timezoneOptions" 
            :key="timezone.value" 
            :value="timezone.value"
          >
            {{ timezone.label }}
          </option>
        </select>
        <div v-if="hasError" class="timezone-error">
          {{ errorMessage }}
        </div>
      </div>

      <!-- Current Time Display -->
      <div v-if="showCurrentTime && selectedTimezone" class="current-time">
        <div class="current-time-label">Current time in selected timezone:</div>
        <div class="current-time-value">{{ currentTime }}</div>
      </div>

      <!-- Timezone Info -->
      <div v-if="showInfo && selectedTimezone" class="timezone-info">
        <div class="timezone-info-item">
          <span class="info-icon">🌍</span>
          <span class="info-text">{{ getTimezoneInfo(selectedTimezone) }}</span>
        </div>
      </div>
    </div>

    <!-- Footer Actions -->
    <template #footer v-if="showActions">
      <div class="timezone-actions">
        <BaseButton
          variant="secondary"
          size="small"
          @click="handleClear"
          :disabled="disabled || !selectedTimezone"
        >
          Clear Selection
        </BaseButton>
        <BaseButton
          variant="primary"
          size="small"
          @click="handleConfirm"
          :disabled="disabled || !selectedTimezone"
        >
          Confirm Timezone
        </BaseButton>
      </div>
    </template>
  </BaseCard>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { isUnifiedTimezone, getCurrentTimeInTimezone, getUnifiedTimezones, formatTimezoneCurrentLabel } from '@/utils/timezone'

// Props definition
const props = defineProps({
  // v-model support
  modelValue: {
    type: String,
    default: ''
  },
  // Card configuration
  title: {
    type: String,
    default: 'Select Timezone'
  },
  label: {
    type: String,
    default: 'Choose your timezone'
  },
  placeholder: {
    type: String,
    default: 'Select a timezone'
  },
  // Display options
  showCurrentTime: {
    type: Boolean,
    default: true
  },
  showInfo: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  // State
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  // Error handling
  errorMessage: {
    type: String,
    default: ''
  },
  // Additional CSS classes
  class: {
    type: String,
    default: ''
  }
})

// Emits definition
const emit = defineEmits(['update:modelValue', 'change', 'confirm', 'clear', 'error'])

// Reactive data
const selectedTimezone = ref(props.modelValue)
const currentTime = ref('')
const timeInterval = ref(null)

// Timezone options from unified list with DST-aware labels
const timezoneOptions = getUnifiedTimezones().map(({ tz }) => ({ value: tz, label: formatTimezoneCurrentLabel(tz) }))

// Computed properties
const cardClasses = computed(() => {
  const classes = ['timezone-selector-card']
  
  if (props.class) {
    classes.push(props.class)
  }
  
  if (props.disabled) {
    classes.push('timezone-selector-card--disabled')
  }
  
  return classes
})

const hasError = computed(() => {
  return props.errorMessage && props.errorMessage.length > 0
})

// Methods
const handleTimezoneChange = (event) => {
  const newValue = event.target.value
  selectedTimezone.value = newValue
  
  console.log('TimezoneSelectorCard: Timezone changed', newValue)
  
  // Emit events
  emit('update:modelValue', newValue)
  emit('change', newValue)
  
  // Start time update if showing current time
  if (props.showCurrentTime && newValue) {
    startTimeUpdate()
  }
}

const handleConfirm = () => {
  if (!selectedTimezone.value) {
    console.warn('TimezoneSelectorCard: Cannot confirm without timezone selection')
    return
  }
  
  console.log('TimezoneSelectorCard: Timezone confirmed', selectedTimezone.value)
  emit('confirm', selectedTimezone.value)
}

const handleClear = () => {
  selectedTimezone.value = ''
  currentTime.value = ''
  
  console.log('TimezoneSelectorCard: Timezone cleared')
  
  // Emit events
  emit('update:modelValue', '')
  emit('clear')
  
  // Stop time update
  stopTimeUpdate()
}

const getTimezoneInfo = (timezone) => {
  if (!isUnifiedTimezone(timezone)) return 'Invalid timezone'
  
  const option = timezoneOptions.find(opt => opt.value === timezone)
  if (!option) return timezone
  
  return option.label
}

const updateCurrentTime = () => {
  if (!selectedTimezone.value) return
  
  try {
    // Format the current time directly in the selected timezone.
    // Important: pass timeZone to the formatter; otherwise it uses the system timezone
    currentTime.value = new Date().toLocaleString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      timeZoneName: 'short',
      timeZone: selectedTimezone.value
    })
  } catch (error) {
    console.error('TimezoneSelector: Error updating current time', error)
    currentTime.value = 'Invalid timezone'
  }
}

const startTimeUpdate = () => {
  if (timeInterval.value) {
    clearInterval(timeInterval.value)
  }
  
  updateCurrentTime()
  timeInterval.value = setInterval(updateCurrentTime, 1000)
}

const stopTimeUpdate = () => {
  if (timeInterval.value) {
    clearInterval(timeInterval.value)
    timeInterval.value = null
  }
}

// Lifecycle
onMounted(() => {
  if (props.showCurrentTime && selectedTimezone.value) {
    startTimeUpdate()
  }
})

onUnmounted(() => {
  stopTimeUpdate()
})

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  selectedTimezone.value = newValue
  if (props.showCurrentTime && newValue) {
    startTimeUpdate()
  } else {
    stopTimeUpdate()
  }
})
</script>

<style scoped>
.timezone-selector-card {
  max-width: 100%;
}

.timezone-selector-card--disabled {
  opacity: 0.6;
  pointer-events: none;
}

.timezone-selector {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.timezone-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.timezone-label {
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 0.9rem;
}

.timezone-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  transition: all 0.2s;
  cursor: pointer;
}

.timezone-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.timezone-select--error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.timezone-select:disabled {
  background: #f9fafb;
  cursor: not-allowed;
  opacity: 0.6;
}

.timezone-error {
  color: #ef4444;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.current-time {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.current-time-label {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.current-time-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.timezone-info {
  padding: 1rem;
  background: #f0f9ff;
  border-radius: 8px;
  border: 1px solid #bae6fd;
}

.timezone-info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.info-icon {
  font-size: 1rem;
}

.info-text {
  font-weight: 500;
}

.timezone-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

/* Responsive design */
@media (max-width: 640px) {
  .timezone-actions {
    flex-direction: column;
  }
  
  .timezone-select {
    padding: 0.6rem;
  }
  
  .current-time,
  .timezone-info {
    padding: 0.75rem;
  }
}
</style>
