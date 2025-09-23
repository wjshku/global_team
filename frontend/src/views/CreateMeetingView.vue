<template>
  <div class="create-meeting-view">
    <BaseCard>
      <template #header>
        <h3 class="card-title">
          <span class="card-icon">📅</span>
          Create Meeting
        </h3>
      </template>

      <form class="form" @submit.prevent="handleSubmit">
        <div class="form-row">
          <label class="label" for="team">Team</label>
          <select id="team" v-model="form.teamId" class="input" required>
            <option disabled value="">-- Select your team --</option>
            <option v-for="team in userTeams" :key="team.id" :value="team.id">{{ team.name }}</option>
          </select>
          <div v-if="!userTeams.length" class="hint">You must belong to a team to create a meeting.</div>
        </div>

        <div class="form-row">
          <TimezoneSelector
            v-model="form.timezone"
            title="Meeting Timezone"
            label="Timezone for scheduling"
            :show-actions="false"
          />
          <div class="hint">Times below are interpreted in the selected timezone and stored as UTC.</div>
        </div>

        <div class="form-row">
          <label class="label" for="title">Title</label>
          <input id="title" v-model="form.title" class="input" type="text" placeholder="e.g., Weekly Standup" required />
        </div>

        <div class="form-row">
          <label class="label" for="description">Description</label>
          <textarea id="description" v-model="form.description" class="textarea" rows="4" placeholder="Optional"></textarea>
        </div>

        <div class="form-row">
          <label class="label">Voting Options</label>
          <div class="option-builder">
            <input v-model="optionDraft.start" class="input" type="datetime-local" />
            <select v-model.number="optionDraft.duration" class="input" style="max-width: 160px;">
              <option :value="30">30 minutes</option>
              <option :value="60">60 minutes</option>
            </select>
            <BaseButton type="button" size="small" variant="secondary" @click="addOption" :disabled="!optionDraft.start">Add Option</BaseButton>
          </div>
          <div v-if="form.options.length === 0" class="hint">Add at least one time option (30 or 60 minutes).</div>
          <ul v-else class="options-list">
            <li v-for="(opt, idx) in form.options" :key="opt.timeSlot" class="option-item">
              <span class="option-text">{{ formatOption(opt) }}</span>
              <BaseButton type="button" size="small" variant="danger" @click="removeOption(idx)">Remove</BaseButton>
            </li>
          </ul>
        </div>

        <div class="actions">
          <BaseButton type="submit" variant="primary" :disabled="isSubmitting || !canSubmit">Create</BaseButton>
          <BaseButton type="button" variant="secondary" @click="goBack">Cancel</BaseButton>
        </div>
      </form>
    </BaseCard>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTeamsStore } from '@/store/modules/teams'
import { useAuthStore } from '@/store/modules/auth'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { meetingsAPI } from '@/api/meetings'
import TimezoneSelector from '@/components/features/TimezoneSelector.vue'
import { getUserTimezone } from '@/utils/timezone'

export default {
  name: 'CreateMeetingView',
  components: { BaseCard, BaseButton, TimezoneSelector },
  setup() {
    const router = useRouter()
    const teamsStore = useTeamsStore()
    const authStore = useAuthStore()

    authStore.initializeAuth()
    if (!teamsStore.allTeams?.length) {
      teamsStore.fetchTeams()
    }

    const currentUserId = computed(() => authStore.currentUser?.id || null)

    const userTeams = computed(() => {
      const all = teamsStore.allTeams || []
      const uid = currentUserId.value
      return uid ? all.filter(t => Array.isArray(t.members) && t.members.includes(uid)) : []
    })

    const nowIsoLocal = () => new Date().toISOString().slice(0, 16)

    const form = ref({
      teamId: '',
      title: '',
      description: '',
      options: [],
      timezone: (authStore.currentUser?.timezone) || getUserTimezone() || 'UTC',
      // votingStart/votingEnd removed
    })

    const isSubmitting = ref(false)

    const optionDraft = ref({ start: nowIsoLocal(), duration: 30 })

    const canSubmit = computed(() => {
      if (!form.value.teamId || !form.value.title) return false
      if (!form.value.options.length) return false
      const team = teamsStore.getTeamById?.(form.value.teamId)
      const uid = currentUserId.value
      return !!(team && uid && Array.isArray(team.members) && team.members.includes(uid))
    })

    const addOption = () => {
      if (!optionDraft.value.start) return
      // Interpret optionDraft.start in the selected timezone and keep it as local ISO without Z; backend will convert using timezone
      const timeSlot = optionDraft.value.start
      if (form.value.options.some(o => o.timeSlot === timeSlot)) return
      form.value.options = [...form.value.options, { timeSlot, duration: optionDraft.value.duration }]
    }

    const removeOption = (index) => {
      form.value.options = form.value.options.filter((_, i) => i !== index)
    }

    const formatOption = (opt) => {
      const d = new Date(opt.timeSlot)
      const pad = (n) => String(n).padStart(2, '0')
      const date = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`
      const time = `${pad(d.getHours())}:${pad(d.getMinutes())}`
      return `${date} ${time} (${opt.duration}m)`
    }

    const handleSubmit = async () => {
      if (!canSubmit.value) return
      try {
        isSubmitting.value = true
        const payload = {
          title: form.value.title,
          description: form.value.description,
          // No scheduledTime until voting is settled
          status: 'voting',
          options: form.value.options,
          timezone: form.value.timezone,
          creatorId: currentUserId.value
        }
        const created = await meetingsAPI.createMeeting(form.value.teamId, payload)
        if (created?.id) {
          router.push({ name: 'meeting', params: { id: created.id } })
        } else {
          router.push({ name: 'meetings' })
        }
      } catch (e) {
        console.error('Create meeting failed', e)
      } finally {
        isSubmitting.value = false
      }
    }

    const goBack = () => {
      router.back()
    }

    return {
      form,
      userTeams,
      isSubmitting,
      canSubmit,
      optionDraft,
      addOption,
      removeOption,
      formatOption,
      handleSubmit,
      goBack
    }
  }
}
</script>

<style scoped>
.create-meeting-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.card-icon {
  font-size: 1.5rem;
}

.form {
  display: grid;
  gap: 1rem;
}

.form-row {
  display: grid;
  gap: 0.5rem;
}

.form-row.grid {
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.label {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.input, .textarea, select.input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text-primary);
}

.textarea {
  resize: vertical;
}

.hint {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.option-builder {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.options-list {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0 0 0;
  display: grid;
  gap: 0.5rem;
}

.option-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
}

.option-text {
  color: var(--color-text-primary);
}

@media (max-width: 768px) {
  .form-row.grid {
    grid-template-columns: 1fr;
  }
}
</style>


