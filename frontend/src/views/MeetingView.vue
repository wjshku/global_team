<template>
  <div class="meeting-view">
    

    <!-- Selectors + Info Side-by-Side -->
    <div class="selectors-and-info">
      <!-- Left Column: Create + Selectors -->
      <section class="left-column">
        <BaseCard class="cta-card">
          <div class="cta-row">
            <router-link :to="{ name: 'meeting-create' }">
              <BaseButton variant="primary" size="small">Create Meeting</BaseButton>
            </router-link>
            <BaseButton
              v-if="canDeleteMeeting && selectedMeetingId"
              variant="danger"
              size="small"
              @click="confirmDelete"
            >
              Delete Meeting
            </BaseButton>
          </div>
        </BaseCard>

        <BaseCard>
          <div class="selectors-grid">
            <!-- Team Selector -->
            <div class="selector">
              <label for="teamSelect" class="selector-label">Select Team</label>
              <select id="teamSelect" v-model="selectedTeamId" class="selector-input">
                <option disabled value="">-- Choose your team --</option>
                <option v-for="team in userTeams" :key="team.id" :value="team.id">
                  {{ team.name }}
                </option>
              </select>
            </div>

            <!-- Meeting Selector -->
            <div class="selector">
              <label for="meetingSelect" class="selector-label">Select Meeting</label>
              <select id="meetingSelect" v-model="selectedMeetingId" class="selector-input" :disabled="!selectedTeamId || teamMeetings.length === 0">
                <option disabled value="">-- Choose a meeting --</option>
                <option v-for="m in teamMeetings" :key="m.id" :value="m.id">
                  {{ m.title }} — {{ formatDateTime(m.scheduledTime || m.scheduledAt) }}
                </option>
              </select>
            </div>
          </div>
        </BaseCard>
      </section>

      <!-- Right Column: Meeting Info -->
      <section v-if="meeting" class="meeting-info-section">
        <BaseCard class="meeting-info-card">
          <template #header>
            <h3 class="card-title">
              <span class="card-icon">ℹ️</span>
              Meeting Information
            </h3>
          </template>
          <div class="meeting-details">
            <div class="meeting-detail-item">
              <span class="detail-label">Title:</span>
              <span class="detail-value">{{ meeting.title }}</span>
            </div>
            <div class="meeting-detail-item">
              <span class="detail-label">Date:</span>
              <span class="detail-value">{{ meeting.scheduledTime ? formatDateTime(meeting.scheduledTime, { timeZone: userTz }) : 'TBD (based on voting)' }}</span>
            </div>
            <div class="meeting-detail-item">
              <span class="detail-label">Status:</span>
              <span class="detail-value" :class="`status-${meeting.status}`">
                {{ meeting.status }}
              </span>
            </div>
          </div>
        </BaseCard>
      </section>
    </div>

    <!-- Main Content Grid -->
    <div class="meeting-content">
      <!-- Meeting Members Section -->
      <section class="members-section">
        <BaseCard class="members-card">
          <template #header>
            <h3 class="card-title">
              <span class="card-icon">👥</span>
              Meeting Participants ({{ meetingMembers.length }})
            </h3>
          </template>
          <div v-if="meetingMembers.length === 0" class="empty-state">
            <p class="empty-message">No participants yet.</p>
          </div>
          <div v-else class="members-list">
            <div
              v-for="member in meetingMembers"
              :key="member.id"
              class="member-item"
            >
              <div class="member-avatar">
                <span class="avatar-text">{{ getInitials(member.name) }}</span>
              </div>
              <div class="member-info">
                <div class="member-name">{{ member.name }}</div>
                <div class="member-timezone">{{ member.timezone }}</div>
              </div>
            </div>
          </div>
        </BaseCard>
      </section>

      <!-- Voting Panel Section -->
      <section class="voting-section">
        <BaseCard class="voting-card">
          <template #header>
            <h3 class="card-title">
              <span class="card-icon">🗳️</span>
              Voting Panel
            </h3>
          </template>
          <VotingPanelCard
            :voting="voting"
            :current-user-id="currentUserId"
            :can-vote="!!currentUserId && meetingMembers.some(m => m.id === currentUserId)"
            :show-actions="true"
            @vote="handleVoteSubmitted"
          />
        </BaseCard>
      </section>

      <!-- Vote Results Section -->
      <section class="results-section">
        <BaseCard class="results-card">
          <template #header>
            <h3 class="card-title">
              <span class="card-icon">📊</span>
              Vote Results
            </h3>
          </template>
          <VoteResultsPanel
            :results="transformedResults"
            :total-votes="totalVotes"
            :can-select-winner="canSelectWinner"
            :raw-id-by-formatted="rawIdByFormatted"
            v-model="selectedWinningOption"
            @end="endVoting"
          />
        </BaseCard>
      </section>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMeetingsStore } from '@/store/modules/meetings'
import { useUIStore } from '@/store/modules/ui'
import { useTeamsStore } from '@/store/modules/teams'
import { useAuthStore } from '@/store/modules/auth'
import { meetingsAPI } from '@/api/meetings'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import VotingPanelCard from '@/components/features/VotingPanelCard.vue'
import VoteResultsPanel from '@/components/features/VoteResultsPanel.vue'
import { formatDateTime } from '@/utils/formatters'

export default {
  name: 'MeetingView',
  components: {
    BaseCard,
    BaseButton,
    VotingPanelCard,
    VoteResultsPanel
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const meetingsStore = useMeetingsStore()
    const uiStore = useUIStore()
    const teamsStore = useTeamsStore()
    const authStore = useAuthStore()
    
    // Route meeting id (optional)
    const meetingId = computed(() => {
      const id = route.params.id
      console.log('MeetingView: Meeting ID from route', id)
      return id
    })
    
    // Selected team/meeting
    const selectedTeamId = ref('')
    const selectedMeetingId = ref('')
    const teamMeetings = ref([])

    // Auth & user
    const currentUserId = computed(() => authStore.currentUser?.id || null)
    const userTz = computed(() => authStore.currentUser?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone)

    // Meeting data
    const meeting = computed(() => meetingsStore.currentMeeting)
    const meetingMembers = computed(() => meetingsStore.meetingMembers)
    const meetingVotes = computed(() => meetingsStore.meetingVotes)
    const voteResults = computed(() => meetingsStore.voteResults)

    const canDeleteMeeting = computed(() => {
      const m = meeting.value
      const uid = currentUserId.value
      return !!(m && uid && m.creatorId === uid)
    })

    // Allow meeting creator to end voting regardless of current voting window
    const canSelectWinner = computed(() => !!canDeleteMeeting.value)
    const selectedWinningOption = ref('')
    const resultRawId = (result) => {
      const match = (voting.value?.options || []).find(o => formatDateTime(o.id) === result.option)
      return match?.id || ''
    }

    const rawIdByFormatted = computed(() => {
      const map = {}
      ;(voting.value?.options || []).forEach(o => { map[formatDateTime(o.id, { timeZone: userTz.value })] = o.id })
      return map
    })

    // Teams filtered by user membership
    const userTeams = computed(() => {
      const all = teamsStore.allTeams || []
      const uid = currentUserId.value
      return uid ? all.filter(t => Array.isArray(t.members) && t.members.includes(uid)) : []
    })

    // Transform results object -> array for display
    const transformedResults = computed(() => {
      const vr = voteResults.value || {}
      const entries = Array.isArray(vr)
        ? vr
        : Object.entries(vr).map(([key, val]) => ({ option: formatDateTime(key, { timeZone: userTz.value }), count: (val && val.votes) || 0, duration: val?.duration }))
      const total = entries.reduce((sum, r) => sum + (r.count || 0), 0)
      return entries.map(r => ({ ...r, percentage: total ? Math.round((r.count || 0) * 100 / total) : 0 }))
    })

    const totalVotes = computed(() => transformedResults.value?.reduce((total, result) => total + result.count, 0) || 0)

    // Build VotingPanelCard props.voting object with voters from meetingVotes
    const voting = computed(() => {
      const vr = voteResults.value || {}
      const votes = meetingVotes.value || []
      let options = Array.isArray(vr)
        ? vr
        : Object.entries(vr).map(([key, val]) => {
            const voters = votes
              .filter(v => v.timeSlot === key)
              .map(v => v.userId)
            return {
              id: key,
            text: formatDateTime(key, { timeZone: userTz.value }),
              votes: (val && val.votes) != null ? val.votes : voters.length,
              duration: val?.duration,
              voters
            }
          })
      // Ensure options are always in chronological order by their UTC id
      options = (options || []).slice().sort((a, b) => {
        const ta = Date.parse(a?.id || '') || 0
        const tb = Date.parse(b?.id || '') || 0
        return ta - tb
      })
      return {
        id: meeting.value?.id,
        title: meeting.value?.title || 'Meeting Voting',
        description: meeting.value?.description || '',
        status: meeting.value?.status || 'open',
        options
      }
    })

    // Methods
    const getInitials = (name) => {
      if (!name) return '?'
      return name.split(' ').map(word => word[0]).join('').toUpperCase()
    }

    const handleVoteSubmitted = async (voteData) => {
      try {
        if (!meeting.value?.id || !currentUserId.value) return
        // Only team members can vote
        const isMember = (meetingMembers.value || []).some(m => m.id === currentUserId.value)
        if (!isMember) {
          uiStore.showNotification({ type: 'error', message: 'Only team members can vote.' })
          return
        }

        // Map optionId to timeSlot expected by API
        const payload = {
          meetingId: meeting.value.id,
          userId: currentUserId.value,
          timeSlot: voteData?.optionId,
          preference: voteData?.preference || 'high'
        }

        await meetingsStore.submitVote(meeting.value.id, payload)
        await Promise.all([
          meetingsStore.fetchMeetingVotes(meeting.value.id),
          meetingsStore.fetchVoteResults(meeting.value.id)
        ])
        uiStore.showNotification({ type: 'success', message: 'Vote submitted successfully!' })
      } catch (e) {
        uiStore.showNotification({ type: 'error', message: 'Failed to submit vote' })
      }
    }

    const confirmDelete = async () => {
      if (!meeting.value?.id) return
      if (!canDeleteMeeting.value) return
      try {
        await meetingsAPI.deleteMeeting(meeting.value.id)
        // Refresh team meetings list and reset selection
        if (selectedTeamId.value) {
          const meetings = await teamsStore.fetchTeamMeetings(selectedTeamId.value)
          teamMeetings.value = Array.isArray(meetings) ? meetings : []
          selectedMeetingId.value = teamMeetings.value[0]?.id || ''
        } else {
          selectedMeetingId.value = ''
        }
      } catch (e) {
        console.error('Failed to delete meeting', e)
      }
    }

    const endVoting = async () => {
      if (!meeting.value?.id || !canSelectWinner.value || !selectedWinningOption.value) return
      try {
        // Update only scheduledTime to avoid touching other fields
        await meetingsAPI.updateMeeting(meeting.value.id, {
          scheduledTime: selectedWinningOption.value
        })
        await meetingsStore.fetchMeeting(meeting.value.id)
        await Promise.all([
          meetingsStore.fetchMeetingVotes(meeting.value.id),
          meetingsStore.fetchVoteResults(meeting.value.id)
        ])
        // Optionally navigate or notify
        uiStore.showNotification?.({ type: 'success', message: 'Voting ended. Meeting scheduled.' })
      } catch (e) {
        console.error('Failed to end voting', e)
        uiStore.showNotification?.({ type: 'error', message: 'Failed to end voting' })
      }
    }

    // Lifecycle
    onMounted(async () => {
      // Initialize auth and teams
      authStore.initializeAuth()
      console.log('[MeetingView] onMounted: currentUser after init', authStore.currentUser)
      await teamsStore.fetchTeams()

      // If coming via route with id, load that meeting and select its team
      if (meetingId.value) {
        await meetingsStore.fetchMeeting(meetingId.value)
        console.log('[MeetingView] Fetched meeting', meetingsStore.currentMeeting)
        const teamId = meetingsStore.currentMeeting?.teamId
        if (teamId) {
          selectedTeamId.value = teamId
          const meetings = await teamsStore.fetchTeamMeetings(teamId)
          teamMeetings.value = Array.isArray(meetings) ? meetings : []
          selectedMeetingId.value = meetingId.value
        }
        await Promise.all([
          meetingsStore.fetchMeetingMembers(meetingId.value),
          meetingsStore.fetchMeetingVotes(meetingId.value),
          meetingsStore.fetchVoteResults(meetingId.value)
        ])
        console.log('[MeetingView] Debug state', {
          currentUserId: currentUserId.value,
          creatorId: meetingsStore.currentMeeting?.creatorId,
          canDeleteMeeting: canDeleteMeeting.value,
          canSelectWinner: canSelectWinner.value
        })
      } else {
        // Preselect first team user belongs to
        if (userTeams.value.length > 0) {
          selectedTeamId.value = userTeams.value[0].id
        }
      }
    })

    // React to team selection -> load meetings
    watch(selectedTeamId, async (newTeamId) => {
      if (!newTeamId) {
        teamMeetings.value = []
        selectedMeetingId.value = ''
        return
      }
      try {
        const meetings = await teamsStore.fetchTeamMeetings(newTeamId)
        teamMeetings.value = Array.isArray(meetings) ? meetings : []
        selectedMeetingId.value = teamMeetings.value[0]?.id || ''
      } catch (e) {
        teamMeetings.value = []
        selectedMeetingId.value = ''
      }
    })

    // React to meeting selection -> load meeting data
    watch(selectedMeetingId, async (newMeetingId) => {
      if (!newMeetingId) return
      await meetingsStore.fetchMeeting(newMeetingId)
      await Promise.all([
        meetingsStore.fetchMeetingMembers(newMeetingId),
        meetingsStore.fetchMeetingVotes(newMeetingId),
        meetingsStore.fetchVoteResults(newMeetingId)
      ])
      // Keep route in sync with selection
      if (route.name !== 'meeting' || route.params.id !== newMeetingId) {
        router.replace({ name: 'meeting', params: { id: newMeetingId } })
      }
    })

    return {
      meetingId,
      meeting,
      selectedTeamId,
      selectedMeetingId,
      teamMeetings,
      userTeams,
      meetingMembers,
      meetingVotes,
      voteResults,
      transformedResults,
      totalVotes,
      voting,
      currentUserId,
      canDeleteMeeting,
      canSelectWinner,
      selectedWinningOption,
      resultRawId,
      rawIdByFormatted,
      userTz,
      getInitials,
      handleVoteSubmitted,
      confirmDelete,
      endVoting,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.meeting-view {
  min-height: 100vh;
  padding: 2rem 0;
}

.selectors-section {
  margin-bottom: 2rem;
  max-width: 100%;
  margin-left: 0;
  margin-right: 0;
}

.cta-row {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.selectors-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.selector {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selector-label {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.selector-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text-primary);
}

.meeting-info-section {
  margin-bottom: 3rem;
  max-width: 100%;
  margin-left: 0;
  margin-right: 0;
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

.meeting-details {
  display: grid;
  gap: 1rem;
}

.meeting-detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border);
}

.detail-label {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.detail-value {
  color: var(--color-text-primary);
}

.status-scheduled {
  color: var(--color-info);
}

.status-active {
  color: var(--color-success);
}

.status-completed {
  color: var(--color-text-secondary);
}

.meeting-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

/* Side-by-side layout for selectors and meeting info */
.selectors-and-info {
  max-width: 1200px;
  margin: 0 auto 2rem auto;
  padding: 0 1rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.members-list {
  display: grid;
  gap: 1rem;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.member-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
}

.avatar-text {
  font-size: 0.9rem;
}

.member-info {
  flex: 1;
}

.member-name {
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 0.25rem;
}

.member-timezone {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.results-content {
  padding: 1rem 0;
}

.results-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: var(--color-background-secondary);
  border-radius: 8px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-label {
  font-weight: 600;
  color: var(--color-text-secondary);
}

.summary-value {
  color: var(--color-text-primary);
  font-weight: 600;
}

.results-chart {
  display: grid;
  gap: 1rem;
}

.result-item {
  display: grid;
  grid-template-columns: 1fr 2fr 80px;
  gap: 1rem;
  align-items: center;
}

.result-option {
  font-weight: 600;
  color: var(--color-text-primary);
}

.result-bar {
  height: 20px;
  background-color: var(--color-border);
  border-radius: 10px;
  overflow: hidden;
}

.result-fill {
  height: 100%;
  background-color: var(--color-primary);
  transition: width 0.3s ease;
}

.result-count {
  text-align: right;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-secondary);
}

.empty-message {
  font-size: 1.1rem;
}

/* Responsive design */
@media (min-width: 768px) {
  .meeting-content {
    grid-template-columns: 1fr 1fr;
  }
  
  .selectors-and-info {
    grid-template-columns: 1fr 1fr;
  }
  
  .members-section {
    grid-column: 1 / -1;
  }

  .selectors-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .result-item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .result-count {
    text-align: left;
  }
}
</style>

