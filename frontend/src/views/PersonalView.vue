<template>
  <div class="personal-view">
    <section class="profile-header">
      <div class="profile-main">
        <div class="avatar">{{ initials }}</div>
        <div class="info">
          <h1 class="name">{{ currentMember?.name || 'Member' }}</h1>
          <div class="meta">
            <span v-if="currentMember?.email">{{ currentMember.email }}</span><span v-if="memberTimezoneLabel">, {{ memberTimezoneLabel }}</span>
          </div>
        </div>
      </div>
      <div class="actions" v-if="isOwner">
        <BaseButton variant="secondary" @click="resetAvailability">Reset</BaseButton>
        <BaseButton variant="primary" @click="saveAvailability" :disabled="!currentMember">Save</BaseButton>
      </div>
    </section>

    <section class="calendar-section" :class="{ 'calendar--readonly': !isOwner }">
      <AvailabilityCalendar
        v-model="availabilityProxy"
        :start-hour="0"
        :end-hour="24"
        :slot-interval="60"
        :show-select-all="isOwner"
        :show-legend="true"
        :show-timezone-selector="true"
        v-model:timezone="selectedTimezone"
        :member-id="null"
        :debug="true"
      />
    </section>

    <section class="teams-section">
      <h2>Your Teams</h2>
      <div v-if="!userTeams.length" class="empty">No teams yet.</div>
      <div class="cards-grid">
        <TeamCard
          v-for="team in userTeamsWithMeetingCounts"
          :key="team.id"
          :team="team"
          :clickable="true"
          :show-actions="false"
          :show-team-actions="false"
          @click="goToTeam(team)"
        />
      </div>
    </section>

    <section class="meetings-section">
      <h2>Upcoming Meetings</h2>
      <div v-if="!transformedUpcomingMeetings.length" class="empty">No upcoming meetings.</div>
      <div class="cards-grid">
        <MeetingCard
          v-for="meeting in transformedUpcomingMeetings"
          :key="meeting.id"
          :meeting="meeting"
          :clickable="true"
          :show-actions="false"
          :show-team-context="true"
          :show-meeting-actions="false"
          @click="goToMeeting(meeting)"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AvailabilityCalendar from '@/components/features/AvailabilityCalendar.vue'
import TeamCard from '@/components/features/TeamCard.vue'
import MeetingCard from '@/components/features/MeetingCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { useMembersStore } from '@/store/modules/members'
import { useTeamsStore } from '@/store/modules/teams'
import { useMeetingsStore } from '@/store/modules/meetings'
import { useAuthStore } from '@/store/modules/auth'
import { getUserTimezone, formatTimezoneCurrentLabel } from '@/utils/timezone'

const router = useRouter()
const route = useRoute()

const membersStore = useMembersStore()
const teamsStore = useTeamsStore()
const meetingsStore = useMeetingsStore()
const authStore = useAuthStore()

// Route member resolution
const routeMemberId = computed(() => route.params.id ? String(route.params.id) : null)
const currentMember = computed(() => {
  if (routeMemberId.value) {
    return membersStore.getMemberById?.(routeMemberId.value) || membersStore.members.find(m => String(m.id) === routeMemberId.value) || null
  }
  return membersStore.currentMember || membersStore.members[0] || null
})

// Ownership and identity
const isOwner = computed(() => {
  const uid = authStore.currentUser?.id
  const mid = currentMember.value?.id
  return uid && mid && String(uid) === String(mid)
})

// Local availability state (object identity preserved)
const availability = ref({})
function replaceAvailability(src) {
  const target = availability.value
  // delete removed keys
  Object.keys(target).forEach((k) => { if (!src || src[k] === undefined) delete target[k] })
  // set new/changed keys
  if (src && typeof src === 'object') {
    Object.keys(src).forEach((k) => { target[k] = !!src[k] })
  }
}

// v-model proxy for AvailabilityCalendar
const availabilityProxy = computed({
  get() { return availability.value },
  set(next) {
    // mutate in place to preserve identity
    const target = availability.value
    // delete keys not present in next
    Object.keys(target).forEach((k) => { if (!next || next[k] === undefined) delete target[k] })
    // set new/changed keys
    if (next && typeof next === 'object') {
      Object.keys(next).forEach((k) => {
        const val = !!next[k]
        if (target[k] !== val) target[k] = val
      })
    }
  }
})

// Timezone handling
const selectedTimezone = ref(null)

// Teams and meetings derived data
const userTeamIds = computed(() => Array.isArray(currentMember.value?.teams) ? currentMember.value.teams.map(String) : [])
const userTeams = computed(() => (teamsStore.allTeams || []).filter(t => userTeamIds.value.includes(String(t.id))))

// Enrich teams with live meeting counts derived from meetings store
const userTeamsWithMeetingCounts = computed(() => {
  const meetings = Array.isArray(meetingsStore.allMeetings) ? meetingsStore.allMeetings : []
  const countsByTeamId = meetings.reduce((acc, meeting) => {
    if (!meeting) return acc
    const teamId = meeting.teamId != null ? String(meeting.teamId) : null
    if (!teamId) return acc
    acc[teamId] = (acc[teamId] || 0) + 1
    return acc
  }, {})
  return userTeams.value.map((team) => {
    const id = team?.id != null ? String(team.id) : ''
    const count = id ? (countsByTeamId[id] || 0) : 0
    return { ...team, meetingCount: count }
  })
})

const upcomingMeetings = computed(() => {
  const now = Date.now()
  const currentMemberId = currentMember.value?.id ? String(currentMember.value.id) : null
  return (meetingsStore.allMeetings || [])
    .filter(m => {
      if (!m) return false
      const inUserTeams = userTeamIds.value.includes(String(m.teamId))
      const isCreator = currentMemberId && String(m.creatorId) === currentMemberId
      return inUserTeams || isCreator
    })
    .filter(m => {
      const ts = m?.scheduledTime || m?.startTime
      if (!ts) return true
      const t = new Date(ts).getTime()
      return Number.isFinite(t) && t > now
    })
    .sort((a, b) => {
      const at = a.scheduledTime ? new Date(a.scheduledTime).getTime() : (a.startTime ? new Date(a.startTime).getTime() : Number.MAX_SAFE_INTEGER)
      const bt = b.scheduledTime ? new Date(b.scheduledTime).getTime() : (b.startTime ? new Date(b.startTime).getTime() : Number.MAX_SAFE_INTEGER)
      return at - bt
    })
})

const transformedUpcomingMeetings = computed(() => {
  return upcomingMeetings.value.map(m => {
    const team = teamsStore.getTeamById?.(String(m.teamId)) || teamsStore.allTeams.find(t => String(t.id) === String(m.teamId)) || null
    const ts = m.scheduledTime || m.startTime
    const iso = ts ? new Date(ts).toISOString() : null
    return { ...m, startTime: iso, scheduledTime: ts ? iso : null, team }
  })
})

// Actions
async function saveAvailability() {
  if (!currentMember.value) return
  await membersStore.updateAvailability(currentMember.value.id, { ...availability.value })
}

function resetAvailability() {
  // Canonical storage is UTC. Use backend availability as-is.
  replaceAvailability(currentMember.value?.availability || {})
}

function goToTeam(team) {
  if (!team?.id) return
  router.push({ name: 'team', params: { id: String(team.id) } })
}

function goToMeeting(meeting) {
  if (!meeting?.id) return
  router.push({ name: 'meeting', params: { id: String(meeting.id) } })
}

// Initialization
onMounted(async () => {
  // Ensure members loaded
  if (!membersStore.allMembers?.length && !membersStore.members?.length) {
    await membersStore.fetchMembers()
  }

  // Set currentMember in store based on authenticated user; fallback to first
  if (!membersStore.currentMember && membersStore.members?.length) {
    const uid = authStore.currentUser?.id
    const byId = uid ? (membersStore.getMemberById?.(uid) || membersStore.members.find(m => String(m.id) === String(uid))) : null
    membersStore.setCurrentMember(byId || membersStore.members[0])
  }

  // Availability is stored in UTC on backend; use as-is
  replaceAvailability(currentMember.value?.availability || {})

  // Initialize timezone
  selectedTimezone.value = authStore.currentUser?.timezone || currentMember.value?.timezone || getUserTimezone()
  console.log('[PersonalView] selectedTimezone before passing to AvailabilityCalendar:', selectedTimezone.value)

  // Load teams and meetings concurrently
  await Promise.all([
    teamsStore.allTeams?.length ? Promise.resolve() : teamsStore.fetchTeams(),
    meetingsStore.allMeetings?.length ? Promise.resolve() : meetingsStore.fetchMeetings()
  ])
})

// Keep availability in sync if viewed member changes; use UTC as-is
watch(currentMember, (next) => {
  replaceAvailability(next?.availability || {})
})

// UI helpers
const initials = computed(() => {
  const name = currentMember.value?.name || ''
  if (!name) return '?'
  return name.split(' ').map(w => w.charAt(0)).join('').toUpperCase().slice(0, 2)
})

// Member timezone display label (shared helper, DST-aware)
const memberTimezoneLabel = computed(() => {
  const tz = currentMember.value?.timezone
  return tz ? formatTimezoneCurrentLabel(tz) : ''
})
</script>

<style scoped>
.personal-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.profile-main { display: flex; align-items: center; gap: 12px; }
.avatar {
  width: 48px; height: 48px; border-radius: 50%;
  background: var(--color-primary, #3b82f6);
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-weight: 700;
}
.info { display: flex; flex-direction: column; }
.name { margin: 0; font-size: 20px; }
.meta { color: #64748b; font-size: 13px; }
.actions { display: flex; gap: 8px; }

.calendar-section { position: relative; }
.calendar--readonly :deep(.time-slot) { pointer-events: none; cursor: default; }
.calendar--readonly { opacity: 0.95; }

.teams-section, .meetings-section { display: flex; flex-direction: column; gap: 12px; }
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
.teams-section .cards-grid {
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}
.empty { color: #94a3b8; font-size: 14px; }

@media (max-width: 640px) {
  .profile-header { flex-direction: column; align-items: flex-start; }
}
</style>

