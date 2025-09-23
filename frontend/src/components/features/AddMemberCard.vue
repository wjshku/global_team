<template>
  <div class="add-member-card">
    <div class="add-member-card__header">
      <h3 class="add-member-card__title">Add Member</h3>
    </div>
    <div class="add-member-card__content">
      <label class="add-member-card__label" for="member-select">Select a member</label>
      <select id="member-select" v-model="selectedId" class="add-member-card__select" :disabled="disabled || options.length === 0">
        <option v-if="options.length === 0" value="" disabled>No available members</option>
        <option v-else value="" disabled>Select a member…</option>
        <option v-for="m in options" :key="m.id" :value="m.id">{{ m.name || m.email || m.id }}</option>
      </select>
      <div class="add-member-card__actions">
        <button class="btn" :disabled="disabled || !selectedId" @click="onAddClick">Add</button>
      </div>
      <p v-if="message" :class="['add-member-card__message', messageType]">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  candidates: { type: Array, default: () => [] },
  disabled: { type: Boolean, default: false },
  successMessage: { type: String, default: '' },
  errorMessage: { type: String, default: '' }
})

const emit = defineEmits(['add'])

const selectedId = ref('')
const message = ref('')
const messageType = ref('')

const options = computed(() => Array.isArray(props.candidates) ? props.candidates : [])

const onAddClick = () => {
  if (!selectedId.value) return
  message.value = ''
  messageType.value = ''
  emit('add', selectedId.value, setSuccess, setError)
}

function setSuccess(text) {
  message.value = text || props.successMessage || 'Member added successfully.'
  messageType.value = 'success'
  selectedId.value = ''
}

function setError(text) {
  message.value = text || props.errorMessage || 'Failed to add member.'
  messageType.value = 'error'
}

watch(() => props.candidates, () => {
  if (!options.value.find(o => String(o.id) === String(selectedId.value))) {
    selectedId.value = ''
  }
})
</script>

<style scoped>
.add-member-card { background: white; border-radius: 12px; padding: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
.add-member-card__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.add-member-card__title { margin: 0; }
.add-member-card__content { display: grid; grid-template-columns: 1fr auto; grid-template-rows: auto auto; gap: 8px 12px; align-items: center; }
.add-member-card__label { grid-column: 1 / -1; font-weight: 600; }
.add-member-card__select { padding: 8px 12px; border: 2px solid var(--border-primary); border-radius: 8px; background: white; min-width: 260px; }
.add-member-card__actions { display: flex; gap: 8px; }
.btn { padding: 8px 12px; border-radius: 8px; border: none; cursor: pointer; background: var(--color-primary); color: #fff; }
.add-member-card__message { grid-column: 1 / -1; margin: 0; font-size: 0.9rem; }
.add-member-card__message.success { color: #065f46; }
.add-member-card__message.error { color: #b91c1c; }
</style>


