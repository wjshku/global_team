<template>
  <BaseCard class="all-meeting-card">
    <template #header>
      <h3 class="card-title">Upcoming Meetings</h3>
    </template>

    <div v-if="loading" class="state state-loading">Loading meetings…</div>
    <div v-else-if="error" class="state state-error">{{ error }}</div>
    <div v-else>
      <div v-if="upcomingMeetings.length === 0" class="state state-empty">No upcoming meetings</div>
      <div v-else class="meetings-grid">
        <router-link
          v-for="m in upcomingMeetings"
          :key="m.id"
          class="mini-card"
          :to="{ name: 'meeting', params: { id: m.id } }"
        >
          <div class="mini-card-header">
            <div class="mini-card-title">{{ m.title || 'Untitled Meeting' }}</div>
          </div>
          <div class="mini-card-body">
            <div class="mini-card-row">
              <span class="row-label">When</span>
              <span class="row-value">
              <template v-if="m.scheduledTime || m.scheduledAt">
                {{ formatDateTime(m.scheduledTime || m.scheduledAt, { timeZone: userTz }) }}
              </template>
                <template v-else>
                  TBD (based on voting)
                </template>
              </span>
            </div>
            <div class="mini-card-row">
              <span class="row-label">Participants</span>
              <span class="row-value">{{ participantsCount }} people</span>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </BaseCard>
  
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import BaseCard from '@/components/common/BaseCard.vue'
import { useTeamsStore } from '@/store/modules/teams'
import { useMembersStore } from '@/store/modules/members'
import { formatDateTime } from '@/utils/formatters'

const props = defineProps({
  teamId: {
    type: [String, Number],
    required: true
  },
  meetings: {
    type: Array,
    default: () => []
  }
})

const teamsStore = useTeamsStore()
const membersStore = useMembersStore()
const authStore = useAuthStore()
const userTz = computed(() => authStore.currentUser?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone)

const loading = ref(false)
const error = ref('')
const localMeetings = ref([])

const normalizeId = (v) => (v == null ? '' : String(v))

const ensureMeetings = async () => {
  try {
    error.value = ''
    loading.value = true
    if (Array.isArray(props.meetings) && props.meetings.length > 0) {
      localMeetings.value = props.meetings.slice()
      return
    }
    const tid = normalizeId(props.teamId)
    if (!tid) {
      localMeetings.value = []
      return
    }
    const fetched = await teamsStore.fetchTeamMeetings(tid)
    localMeetings.value = Array.isArray(fetched) ? fetched : []
  } catch (e) {
    error.value = e?.message || 'Failed to load meetings'
    localMeetings.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // Make sure members are available for participant counts
  if (!membersStore.allMembers || membersStore.allMembers.length === 0) {
    membersStore.fetchMembers()
  }
  ensureMeetings()
  console.log('[AllMeetingCard] mounted', {
    teamId: props.teamId,
    meetings: props.meetings,
    localMeetings: localMeetings.value
  })
})

watch(() => props.teamId, (nid, oid) => {
  console.log('[AllMeetingCard] teamId changed', { old: oid, new: nid })
  ensureMeetings()
})

watch(() => props.meetings, (next, prev) => {
  console.log('[AllMeetingCard] props.meetings changed', {
    prevLen: Array.isArray(prev) ? prev.length : 'n/a',
    nextLen: Array.isArray(next) ? next.length : 'n/a'
  })
  if (Array.isArray(next) && next.length > 0) {
    localMeetings.value = next.slice()
  } else {
    ensureMeetings()
  }
}, { deep: true })

watch(localMeetings, (val) => {
  console.log('[AllMeetingCard] localMeetings updated', {
    length: Array.isArray(val) ? val.length : 'n/a',
    sample: Array.isArray(val) && val[0] ? { id: val[0].id, teamId: val[0].teamId, title: val[0].title, scheduledTime: val[0].scheduledTime || val[0].scheduledAt } : null
  })
})

const baseMeetings = computed(() => {
  const provided = Array.isArray(props.meetings) && props.meetings.length > 0
  return provided ? props.meetings : localMeetings.value
})

const upcomingMeetings = computed(() => {
  const tid = normalizeId(props.teamId)
  const now = Date.now()
  const filtered = (baseMeetings.value || []).filter(m => {
    const teamOk = normalizeId(m?.teamId) === tid
    if (!teamOk) return false
    const ts = Date.parse(m?.scheduledTime || m?.scheduledAt || '')
    // Keep unscheduled (voting) or scheduled in the future
    return isNaN(ts) || ts >= now
  })
  const withKey = filtered.map(m => ({
    m,
    t: Date.parse(m?.scheduledTime || m?.scheduledAt || '')
  }))
  withKey.sort((a, b) => {
    const aUn = isNaN(a.t)
    const bUn = isNaN(b.t)
    if (aUn && bUn) return 0
    if (aUn) return 1 // unscheduled last
    if (bUn) return -1
    return a.t - b.t
  })
  const result = withKey.map(x => x.m)
  console.log('[AllMeetingCard] upcomingMeetings computed', {
    inputLen: baseMeetings.value?.length || 0,
    outputLen: result.length
  })
  return result
})

const teamMembers = computed(() => {
  const team = teamsStore.getTeamById?.(props.teamId)
  if (!team || !Array.isArray(team.members)) return []
  return team.members
    .map(entry => {
      if (entry && typeof entry === 'object') return entry
      return membersStore.getMemberById?.(entry) || { id: entry, name: String(entry) }
    })
    .filter(Boolean)
})

const participantsCount = computed(() => {
  // Currently using team-wide member count as participants for each meeting
  return teamMembers.value.length
})

// Using unified date-time formatter with timezone handled in util

</script>

<style scoped>
.all-meeting-card {
  display: block;
}

.card-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.state {
  padding: 1rem;
  color: var(--text-secondary);
}

.state-error {
  color: var(--color-danger);
}

.meetings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 0.75rem;
}

.mini-card {
  display: block;
  text-decoration: none;
  color: inherit;
  border: 1px solid var(--border-primary);
  border-radius: 8px;
  padding: 0.75rem;
  background: var(--bg-primary);
  transition: box-shadow 0.15s ease, transform 0.15s ease;
}

.mini-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.mini-card-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.mini-card-body {
  display: grid;
  gap: 0.35rem;
}

.mini-card-row {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.row-label {
  color: var(--text-secondary);
}

.row-value {
  color: var(--text-primary);
  text-align: right;
}

.time-sep {
  display: inline-block;
  margin: 0 0.25rem;
  color: var(--text-tertiary);
}

@media (max-width: 640px) {
  .mini-card-row {
    flex-direction: column;
    align-items: flex-start;
  }
  .row-value { text-align: left; }
}
</style>


