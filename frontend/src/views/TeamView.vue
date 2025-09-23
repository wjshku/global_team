<template>
  <div class="team-view">
    <!-- Header: Team selector -->
    <div class="team-view__header">
      <h1 class="team-view__title">Teams</h1>
      <div class="team-view__selector">
        <label for="team-select" class="team-view__label">Select Team</label>
        <select
          id="team-select"
          v-model="selectedTeamId"
          class="team-view__select"
          :disabled="teamsLoading || userTeams.length === 0"
        >
          <option v-if="userTeams.length === 0" value="" disabled>
            No teams available
          </option>
          <option
            v-for="team in userTeams"
            :key="team.id"
            :value="team.id"
          >
            {{ team.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Team details -->
    <div v-if="currentTeam" class="team-view__details">
      <div class="team-card">
        <div class="team-card__header">
          <h2 class="team-card__title">{{ currentTeam.name }}</h2>
          <div class="team-card__meta">
            <span class="team-card__meta-item">Timezone: {{ currentTeam.timezone }}</span>
            <span class="team-card__meta-sep">•</span>
            <span class="team-card__meta-item">Members: {{ currentTeam.memberCount ?? currentTeam.members?.length ?? 0 }}</span>
          </div>
          <div class="section-actions" v-if="isAdmin">
            <button class="btn btn--secondary" @click="onDeleteTeam" :disabled="teamsLoading">Delete Team</button>
          </div>
        </div>
        <p class="team-card__desc">{{ currentTeam.description }}</p>
      </div>
    </div>

    <!-- Availability and meetings layout -->
    <div class="team-view__content" v-if="currentTeam">
      <div class="team-view__calendar calendar--readonly">
        <div class="section-header">
          <h3>Group Availability</h3>
        </div>
        <AvailabilityCalendar
          ref="calendarRef"
          :model-value="{} /* boolean model unused in heatmap mode */"
          :start-hour="0"
          :end-hour="24"
          :slot-interval="60"
          :show-select-all="false"
          :show-legend="true"
          :heatmap-data="availabilityCounts"
          :heatmap-max="totalMembersCount"
          :slot-members-info="slotMembersInfo"
          :show-timezone-selector="true"
          v-model:timezone="selectedTimezone"
          :base-timezone="currentTeam?.timezone || authStore.currentUser?.timezone"
          @hover-info="onHoverInfo"
        />
      </div>

      <div class="team-view__meetings">
        <div v-if="isAdmin" class="section-header">
        </div>
        <AddMemberCard
          v-if="isAdmin"
          :candidates="addableMembers"
          :disabled="teamsLoading || !currentTeam"
          @add="onAddMember"
        />
        <div class="spaced-section">
          <AllMeetingCard
            v-if="selectedTeamId"
            :team-id="selectedTeamId"
            :meetings="teamMeetings"
          />
        </div>
        
        <!-- Availability Details (below meetings) -->
        <div class="availability-details" v-if="hoveredInfo">
          <div class="section-header">
            <h3>Availability Details</h3>
          </div>
          <div class="hover-panel__meta" v-if="hoveredInfo.timeLabel">
            <span class="chip">{{ hoveredInfo.timeLabel }}</span>
            <span class="dot">•</span>
            <span class="chip">Avail: {{ hoveredInfo.available?.length || 0 }}</span>
            <span class="dot">•</span>
            <span class="chip">Unavail: {{ hoveredInfo.unavailable?.length || 0 }}</span>
          </div>
          <div class="availability-details__content">
            <div class="hover-list">
              <div class="hover-list__title">Available</div>
              <div class="hover-list__empty" v-if="!hoveredInfo.available || !hoveredInfo.available.length">—</div>
              <ul class="hover-list__items" v-else>
                <li v-for="p in hoveredInfo.available" :key="p.id" class="hover-list__item">{{ p.name }}</li>
              </ul>
            </div>
            <div class="hover-list">
              <div class="hover-list__title">Unavailable</div>
              <div class="hover-list__empty" v-if="!hoveredInfo.unavailable || !hoveredInfo.unavailable.length">—</div>
              <ul class="hover-list__items" v-else>
                <li v-for="p in hoveredInfo.unavailable" :key="p.id" class="hover-list__item">{{ p.name }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import { useTeamsStore } from '@/store/modules/teams'
import { useMembersStore } from '@/store/modules/members'
import { useRouter } from 'vue-router'
import AvailabilityCalendar from '@/components/features/AvailabilityCalendar.vue'
import AllMeetingCard from '@/components/features/AllMeetingCard.vue'
import AddMemberCard from '@/components/features/AddMemberCard.vue'

// Stores
const authStore = useAuthStore()
const teamsStore = useTeamsStore()
const membersStore = useMembersStore()
const router = useRouter()

// Local state
const selectedTeamId = ref('')
const calendarRef = ref(null)
const selectedTimezone = ref(null)
const hoveredInfo = ref(null)
const teamMeetings = ref([])

// Load initial data
onMounted(async () => {
  // Debug: log current route at mount
  try {
    const r = router?.currentRoute?.value
    console.log('[TeamView] current route at mount', r ? {
      path: r.path,
      params: r.params,
      query: r.query,
      name: r.name,
      fullPath: r.fullPath,
      meta: r.meta
    } : 'no route')
  } catch (_) {}

  if (!teamsStore.allTeams.length) await teamsStore.fetchTeams()
  if (!membersStore.allMembers.length) await membersStore.fetchMembers()

  // Default to first user team
  if (!selectedTeamId.value && userTeams.value.length) {
    // Prefer team where the logged-in user is admin if available; else first
    const uid = authStore.currentUser?.id
    const preferred = userTeams.value.find(t => t.admin === uid) || userTeams.value[0]
    selectedTeamId.value = preferred.id
    console.log('[TeamView] defaulted selectedTeamId', {
      selectedTeamId: selectedTeamId.value,
    })
  }

  // Load meetings for the initially selected team
  if (selectedTeamId.value) {
    try {
      const list = await teamsStore.fetchTeamMeetings(selectedTeamId.value)
      teamMeetings.value = Array.isArray(list) ? list : []
    } catch (_) {
      teamMeetings.value = []
    }
  }

  // Debug: print fetched teams info
  console.log('[TeamView] teams loaded', {
    selectedTeamId:selectedTeamId.value,
    teamMeetings: teamMeetings.value
  })

  // Initialize timezone selection with user's current timezone
  selectedTimezone.value = authStore.currentUser?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone
})

// Derived data
const currentUserId = computed(() => authStore.currentUser?.id || null)
const teamsLoading = computed(() => teamsStore.isLoading)

const userTeams = computed(() => {
  const uid = currentUserId.value
  if (!uid) return []
  return teamsStore.allTeams
    .filter(t => Array.isArray(t.members) && t.members.map(String).includes(String(uid)))
    .slice()
    .sort((a, b) => (a.name || '').localeCompare(b.name || ''))
})

const currentTeam = computed(() => {
  return teamsStore.getTeamById(selectedTeamId.value)
})

const isAdmin = computed(() => {
  const uid = authStore.currentUser?.id
  const team = currentTeam.value
  return !!uid && team && team.admin === uid
})

// Keep store's current team in sync
watch(selectedTeamId, (newId) => {
  const team = teamsStore.getTeamById(newId)
  // Debug: log selected team id before passing to AllMeetingCard
  console.log('[TeamView] selectedTeamId changed', {
    selectedTeamId: newId,
    resolvedTeam: team,
  })
  if (team) teamsStore.setCurrentTeam(team)
  // Fetch meetings whenever team selection changes
  if (newId) {
    teamsStore.fetchTeamMeetings(newId)
      .then(list => { teamMeetings.value = Array.isArray(list) ? list : [] })
      .catch(() => { teamMeetings.value = [] })
  } else {
    teamMeetings.value = []
  }
})

// Members that can be added (exclude those already in team)
const addableMembers = computed(() => {
  const team = currentTeam.value
  if (!team) return []
  const existing = new Set((team.members || []).map(String))
  return membersStore.allMembers
    .filter(m => !existing.has(String(m.id)))
    .map(m => ({ id: m.id, name: m.name, email: m.email }))
    .sort((a, b) => (a.name || '').localeCompare(b.name || ''))
})

// Aggregate team availability counts per slot and common intersection (for reference)
const teamAvailability = computed(() => {
  const team = currentTeam.value
  if (!team) return {}

  const memberIds = Array.isArray(team.members) ? team.members : []
  const totalMembers = memberIds.length
  if (totalMembers === 0) return {}

  const slotCounts = {}

  // 1) From members store availability map (counts per slot)
  memberIds.forEach(memberId => {
    const av = membersStore.getAvailability[memberId]
    if (av) {
      Object.keys(av).forEach(key => {
        if (av[key]) slotCounts[key] = (slotCounts[key] || 0) + 1
      })
    }
  })

  // 2) From member objects (if they carry availability)
  membersStore.allMembers
    .filter(m => memberIds.includes(m.id) && m.availability)
    .forEach(m => {
      Object.keys(m.availability).forEach(key => {
        if (m.availability[key]) slotCounts[key] = (slotCounts[key] || 0) + 1
      })
    })

  // Keep only slots where everyone is available
  const commonAvailability = {}
  Object.keys(slotCounts).forEach(key => {
    if (slotCounts[key] >= totalMembers) commonAvailability[key] = true
  })

  return commonAvailability
})

// Counts for heatmap
const availabilityCounts = computed(() => {
  const team = currentTeam.value
  if (!team) return {}

  const memberIds = Array.isArray(team.members) ? team.members : []
  const slotCounts = {}

  // From members store availability map
  memberIds.forEach(memberId => {
    const av = membersStore.getAvailability[memberId]
    if (av) {
      Object.keys(av).forEach(key => {
        if (av[key]) slotCounts[key] = (slotCounts[key] || 0) + 1
      })
    }
  })

  // From member objects (fallback)
  membersStore.allMembers
    .filter(m => memberIds.includes(m.id) && m.availability)
    .forEach(m => {
      Object.keys(m.availability).forEach(key => {
        if (m.availability[key]) slotCounts[key] = (slotCounts[key] || 0) + 1
      })
    })

  return slotCounts
})

const totalMembersCount = computed(() => {
  const team = currentTeam.value
  return Array.isArray(team?.members) ? team.members.length : 0
})

// Build per-slot member info for tooltip (include ALL slots so unavailable = everyone not available)
const slotMembersInfo = computed(() => {
  const team = currentTeam.value
  if (!team) return {}
  const memberIds = Array.isArray(team.members) ? team.members : []
  const byId = new Map(membersStore.allMembers.map(m => [m.id, m]))

  // Keep in sync with AvailabilityCalendar props used here
  const startHour = 0
  const endHour = 24
  const slotInterval = 60
  const totalMinutes = Math.max(0, (endHour - startHour) * 60)
  const totalSlotsPerDay = Math.max(1, Math.round(totalMinutes / slotInterval))

  const info = {}
  for (let d = 0; d < 7; d += 1) {
    for (let s = 0; s < totalSlotsPerDay; s += 1) {
      const key = `day_${d}_slot_${s}`
      const available = []
      const unavailable = []
      memberIds.forEach(id => {
        const member = byId.get(id)
        const av = membersStore.getAvailability[id] || member?.availability || {}
        const isAvail = !!av[key]
        if (member) {
          (isAvail ? available : unavailable).push({ id: member.id, name: member.name || member.id })
        }
      })
      info[key] = { available, unavailable }
    }
  }

  return info
})

// Upcoming meetings handled by AllMeetingCard

// Handle hover info from AvailabilityCalendar
const onHoverInfo = (payload) => {
  hoveredInfo.value = payload
}

// Read-only calendar: block interaction via style (see scoped CSS below)

// Formatting helpers moved into AllMeetingCard

// Admin-only delete action
const onDeleteTeam = async () => {
  if (!isAdmin.value || !currentTeam.value) return
  try {
    await teamsStore.deleteTeam(currentTeam.value.id)
    // After deletion, refresh teams if needed and redirect
    if (!teamsStore.allTeams.length) await teamsStore.fetchTeams()
    router.push({ name: 'teams' })
  } catch (e) {
    console.error('Failed to delete team', e)
  }
}

// Add member flow (admin only)
const onAddMember = async (memberId, onSuccess, onError) => {
  if (!isAdmin.value || !currentTeam.value) return
  try {
    await teamsStore.addMember(currentTeam.value.id, memberId)
    // UI updates immediately via store replacement of currentTeam; also recompute derived data
    onSuccess && onSuccess('Member added successfully.')
  } catch (err) {
    const msg = String(err?.message || '')
    if (msg.includes('409')) {
      onError && onError('Member already in team.')
    } else if (msg.includes('403')) {
      onError && onError('You do not have permission to add members.')
    } else if (msg.includes('404')) {
      onError && onError('Team or member not found.')
    } else {
      onError && onError('Failed to add member. Please try again.')
    }
  }
}
</script>

<style scoped>
.team-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px;
}

.team-view__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.team-view__title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.team-view__selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.team-view__label {
  font-weight: 600;
  flex-shrink: 0;
}

.team-view__select {
  padding: 8px 12px;
  border: 2px solid var(--border-primary);
  border-radius: 8px;
  background: white;
  min-width: 320px;
}

.team-view__details {
  display: flex;
}

.team-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.team-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.team-card__title { margin: 0; }

.team-card__meta { color: var(--text-secondary); font-size: 0.9rem; }
.team-card__meta-sep { margin: 0 6px; }

.team-card__desc { margin-top: 8px; color: var(--text-secondary); }

.team-view__content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}

.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.section-actions { display: flex; gap: 8px; }
.btn { padding: 6px 10px; border-radius: 6px; border: none; cursor: pointer; background: var(--color-primary); color: #fff; }
.btn--secondary { background: #64748b; }

.meetings-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }
.meeting-item { background: white; border-radius: 10px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); }
.meeting-item__link { display: block; color: inherit; text-decoration: none; }
.meeting-item__title { font-weight: 600; margin-bottom: 4px; }
.meeting-item__meta { color: var(--text-secondary); font-size: 0.9rem; }
.meeting-item .dot { margin: 0 6px; }
.meeting-item__participants { margin-top: 6px; font-size: 0.9rem; color: var(--text-secondary); }

/* Hover info panel */
.team-view__hover-panel {
  background: white;
  border: 1px solid var(--border-primary);
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.hover-panel__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.hover-panel__title { font-weight: 700; }
.hover-panel__meta { color: var(--text-secondary); display: flex; align-items: center; gap: 6px; }
.chip { background: #f1f5f9; border-radius: 999px; padding: 2px 8px; font-size: 12px; }
.hover-panel__content { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.hover-list { display: flex; flex-direction: column; gap: 6px; }
.hover-list__title { font-weight: 600; color: #334155; }
.hover-list__empty { color: var(--text-secondary); }
.hover-list__items { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 4px; max-height: 160px; overflow: auto; }
.hover-list__item { padding: 6px 8px; background: #f8fafc; border-radius: 6px; }

@media (max-width: 1024px) {
  .team-view__content { grid-template-columns: 1fr; }
}

/* Read-only calendar: disable pointer events on slots */
/* keep clicks disabled via component logic; allow hover tooltips */

/* Local spacing helpers */
.spaced-section { margin-top: 12px; }
</style>