<template>
  <section class="create-team-view">
    <BaseCard>
      <h1 class="title">Create Team</h1>
      <form class="form" @submit.prevent="onSubmit">
        <div class="field">
          <label for="name">Team Name</label>
          <input
            id="name"
            v-model.trim="form.name"
            type="text"
            :maxlength="100"
            placeholder="e.g. Product Engineering"
            :disabled="isSubmitting"
            required
          />
          <p v-if="errors.name" class="error">{{ errors.name }}</p>
        </div>

        <div class="field">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model.trim="form.description"
            :maxlength="500"
            placeholder="What is this team about?"
            :disabled="isSubmitting"
            rows="4"
          />
          <p v-if="errors.description" class="error">{{ errors.description }}</p>
        </div>

        

        <div class="actions">
          <BaseButton type="submit" :disabled="isSubmitting || hasErrors">
            {{ isSubmitting ? 'Creating…' : 'Create Team' }}
          </BaseButton>
        </div>

        <p v-if="submitError" class="submit-error">{{ submitError }}</p>
      </form>
    </BaseCard>
  </section>
  
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useTeamsStore } from '@/store/modules/teams'
import { useAuthStore } from '@/store/modules/auth'

const router = useRouter()
const teamsStore = useTeamsStore()
const authStore = useAuthStore()

const form = reactive({
  name: '',
  description: ''
})

const errors = reactive({ name: '', description: '' })

const isSubmitting = computed(() => teamsStore.isLoading)
const submitError = computed(() => teamsStore.error)

const hasErrors = computed(() => {
  return !!(errors.name || errors.description)
})

function validate() {
  errors.name = ''
  errors.description = ''

  if (!form.name || !form.name.trim()) {
    errors.name = 'Team name is required.'
  } else if (form.name.length > 100) {
    errors.name = 'Team name must be 100 characters or fewer.'
  }

  if (form.description && form.description.length > 500) {
    errors.description = 'Description must be 500 characters or fewer.'
  }
}

async function onSubmit() {
  validate()
  if (hasErrors.value) return

  const creatorId = authStore.currentUser?.id || null
  const payload = {
    name: form.name.trim(),
    description: form.description.trim(),
    // Ensure creator is a member if available to avoid access guard issues later
    ...(creatorId ? { members: [creatorId], admin: creatorId } : {})
  }

  try {
    const created = await teamsStore.createTeam(payload)
    // Navigate to Teams list (team view is member-guarded)
    router.push({ name: 'teams' })
  } catch (e) {
    // Error already reflected via teamsStore.error
  }
}
</script>

<style scoped>
.create-team-view { display: flex; flex-direction: column; gap: 16px; }
.title { margin: 0 0 8px 0; font-size: 1.5rem; font-weight: 700; }
.form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field input, .field textarea { padding: 10px 12px; border: 1px solid #e2e8f0; border-radius: 8px; }
.actions { margin-top: 4px; }
.error { color: #b91c1c; font-size: 0.9rem; }
.submit-error { color: #b91c1c; margin-top: 8px; }
</style>


