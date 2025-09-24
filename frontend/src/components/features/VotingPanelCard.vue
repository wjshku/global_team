<!-- VotingPanelCard.vue - Component for displaying voting options and results -->
<template>
  <BaseCard 
    :class="cardClasses"
    :clickable="clickable"
    @click="handleCardClick"
  >
    <!-- Voting Header -->
    <template #header>
      <div class="voting-header">
        <div class="voting-icon">
          🗳️
        </div>
        <div class="voting-info">
          <h3 class="voting-title">{{ voting.title || 'Voting Panel' }}</h3>
          <div class="voting-meta">
            <span class="vote-count">{{ totalVotes }} votes</span>
          </div>
        </div>
        <div class="voting-status" v-if="showStatus">
          <div class="status-indicator" :class="statusClass"></div>
          <span class="status-text">{{ statusText }}</span>
        </div>
      </div>
    </template>

    <!-- Timezone selector for viewing options -->
    <div class="voting-timezone">
      <select v-model="displayTimezone" class="timezone-select">
        <option v-for="tz in timezoneChoices" :key="tz.value" :value="tz.value">{{ tz.label }}</option>
      </select>
    </div>

    <!-- Voting Content -->
    <div class="voting-content">
      <!-- Voting Description -->
      <div v-if="voting.description" class="voting-description">
        <p>{{ voting.description }}</p>
      </div>

      <!-- Voting Options -->
      <div class="voting-options">
        <div 
          v-for="option in votingOptions"
          :key="option.id"
          class="voting-option"
          :class="getOptionClasses(option)"
          @click.stop="handleOptionClick(option)"
        >
          <div class="option-content">
            <div class="option-text">{{ formatOptionText(option) }}</div>
            <div v-if="option.description" class="option-description">{{ option.description }}</div>
          </div>
          <div class="option-votes">
            <div class="vote-count">{{ option.votes || 0 }}</div>
            <div class="vote-percentage">{{ getVotePercentage(option) }}%</div>
          </div>
          <div v-if="isUserVote(option)" class="user-vote-indicator">
            ✓
          </div>
        </div>
      </div>

      <!-- Voting Stats -->
      <div v-if="showStats" class="voting-stats">
        <div class="stat-item">
          <span class="stat-icon">👥</span>
          <div class="stat-content">
            <div class="stat-value">{{ totalVotes }}</div>
            <div class="stat-label">Total Votes</div>
          </div>
        </div>
        <div class="stat-item">
          <span class="stat-icon">⏰</span>
          <div class="stat-content">
            <div class="stat-value">{{ votingOptions.length }}</div>
            <div class="stat-label">Options</div>
          </div>
        </div>
        <div class="stat-item" v-if="voting.participants">
          <span class="stat-icon">🎯</span>
          <div class="stat-content">
            <div class="stat-value">{{ voting.participants.length }}</div>
            <div class="stat-label">Participants</div>
          </div>
        </div>
      </div>

      <!-- Voting Actions -->
      <div v-if="showActions" class="voting-actions">
        <BaseButton
          v-if="!hasUserVoted"
          variant="primary"
          size="small"
          @click.stop="handleVote"
          :disabled="!canCastVote"
        >
          Cast Vote
        </BaseButton>
        <BaseButton
          v-if="canChangeVote && hasUserVoted"
          variant="secondary"
          size="small"
          @click.stop="handleChangeVote"
        >
          Change Vote
        </BaseButton>
        <BaseButton
          v-if="canCloseVoting"
          variant="danger"
          size="small"
          @click.stop="handleCloseVoting"
        >
          Close Voting
        </BaseButton>
        <div v-if="!canVote && !hasUserVoted" class="vote-hint" style="font-size: 0.85rem; color: var(--color-text-secondary);">
          You are not eligible to vote.
        </div>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { formatDate } from '@/utils/formatters'
import { getUnifiedTimezones, formatTimezoneCurrentLabel, getUserTimezone } from '@/utils/timezone'

// Props definition
const props = defineProps({
  voting: {
    type: Object,
    required: true,
    default: () => ({})
  },
  clickable: {
    type: Boolean,
    default: false
  },
  showStatus: {
    type: Boolean,
    default: true
  },
  showStats: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  canVote: {
    type: Boolean,
    default: true
  },
  canChangeVote: {
    type: Boolean,
    default: true
  },
  canViewResults: {
    type: Boolean,
    default: true
  },
  canCloseVoting: {
    type: Boolean,
    default: false
  },
  currentUserId: {
    type: String,
    default: null
  }
})

// Emits definition
const emit = defineEmits(['click', 'vote', 'change-vote', 'close-voting'])

// Local state
const selectedOption = ref(null)
const displayTimezone = ref(getUserTimezone() || 'UTC')
const timezoneChoices = getUnifiedTimezones().map(({ tz }) => ({ value: tz, label: formatTimezoneCurrentLabel(tz) }))

// Computed properties
const cardClasses = computed(() => {
  const classes = ['voting-panel-card']
  
  if (props.clickable) {
    classes.push('voting-panel-card--clickable')
  }
  
  if (isVotingClosed.value) {
    classes.push('voting-panel-card--closed')
  }
  
  return classes
})

const votingOptions = computed(() => {
  return props.voting.options || []
})

const totalVotes = computed(() => {
  return votingOptions.value.reduce((total, option) => total + (option.votes || 0), 0)
})

const hasUserVoted = computed(() => {
  if (!props.currentUserId) return false
  return votingOptions.value.some(option => 
    option.voters && option.voters.includes(props.currentUserId)
  )
})

const userVote = computed(() => {
  if (!props.currentUserId) return null
  return votingOptions.value.find(option => 
    option.voters && option.voters.includes(props.currentUserId)
  )
})

const isVotingClosed = computed(() => {
  return props.voting.status === 'closed'
})

const statusClass = computed(() => {
  if (isVotingClosed.value) return 'status-indicator--closed'
  if (hasUserVoted.value) return 'status-indicator--voted'
  return 'status-indicator--open'
})

const statusText = computed(() => {
  if (isVotingClosed.value) return 'Closed'
  if (hasUserVoted.value) return 'Voted'
  return 'Open'
})

const canCastVote = computed(() => {
  return props.canVote && !!selectedOption.value
})

// Watch for changes in voting data to reset selection
watch(() => props.voting, () => {
  // Reset selection when voting data changes (e.g., after successful vote)
  selectedOption.value = null
}, { deep: true })

// Methods
const handleCardClick = (event) => {
  console.log('VotingPanelCard: Card clicked', props.voting)
  emit('click', props.voting)
}

const handleOptionClick = (option) => {
  if (!props.canVote || isVotingClosed.value) return
  
  console.log('VotingPanelCard: Option clicked', option)
  selectedOption.value = option
}

const handleVote = (event) => {
  if (!selectedOption.value) return
  
  console.log('VotingPanelCard: Vote cast', selectedOption.value)
  emit('vote', {
    votingId: props.voting.id,
    optionId: selectedOption.value.id,
    userId: props.currentUserId
  })
  
  // Clear selection after voting to prevent double-voting
  selectedOption.value = null
}

const handleChangeVote = (event) => {
  // Allow user to change vote by selecting a new option and submitting immediately
  if (!selectedOption.value) return
  console.log('VotingPanelCard: Change vote to', selectedOption.value)
  emit('vote', {
    votingId: props.voting.id,
    optionId: selectedOption.value.id,
    userId: props.currentUserId
  })
  selectedOption.value = null
}

const handleCloseVoting = (event) => {
  console.log('VotingPanelCard: Close voting clicked', props.voting)
  emit('close-voting', props.voting)
}

const getOptionClasses = (option) => {
  const classes = ['voting-option']
  
  if (selectedOption.value && selectedOption.value.id === option.id) {
    classes.push('voting-option--selected')
  }
  
  if (isUserVote(option)) {
    classes.push('voting-option--user-vote')
  }
  
  if (isVotingClosed.value) {
    classes.push('voting-option--closed')
  }
  
  return classes
}

const isUserVote = (option) => {
  if (!props.currentUserId) return false
  return option.voters && option.voters.includes(props.currentUserId)
}

const getVotePercentage = (option) => {
  if (totalVotes.value === 0) return 0
  return Math.round((option.votes || 0) / totalVotes.value * 100)
}

// Removed deadline formatting; no start/end time logic

function formatOptionText(option) {
  // option.id is UTC ISO timeSlot. Convert to selected timezone for display
  try {
    const utcDate = new Date(option.id)
    // Build a formatted string in displayTimezone without changing Date object TZ
    const str = utcDate.toLocaleString('en-US', {
      year: 'numeric', month: 'short', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hour12: false,
      timeZone: displayTimezone.value
    })
    const dur = option.duration ? ` (${option.duration}m)` : ''
    return `${str}${dur}`
  } catch (e) {
    return option.text || option.id
  }
}
</script>

<style scoped>
.voting-panel-card {
  transition: all 0.2s ease;
}

.voting-panel-card--clickable {
  cursor: pointer;
}

.voting-panel-card--clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.voting-panel-card--closed {
  opacity: 0.8;
  border-left: 4px solid #6b7280;
}

.voting-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.voting-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.voting-info {
  flex: 1;
  min-width: 0;
}

.voting-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
}

.voting-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.vote-count {
  font-weight: 500;
}

.voting-deadline {
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.voting-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-indicator--open {
  background: #10b981;
}

.status-indicator--voted {
  background: var(--color-primary);
}

.status-indicator--closed {
  background: #6b7280;
}

.status-text {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.voting-timezone {
  display: flex;
  justify-content: flex-end;
  padding: 0 0.5rem 0.5rem 0.5rem;
}

.timezone-select {
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
}

.voting-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.voting-description {
  color: var(--color-text-primary);
  line-height: 1.6;
}

.voting-description p {
  margin: 0;
}

.voting-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.voting-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.voting-option:hover {
  border-color: var(--color-primary);
  background: #f8fafc;
}

.voting-option--selected {
  border-color: var(--color-primary);
  background: #eff6ff;
}

.voting-option--user-vote {
  border-color: var(--color-primary);
  background: #eff6ff;
}

.voting-option--closed {
  cursor: default;
  opacity: 0.7;
}

.voting-option--closed:hover {
  border-color: #e2e8f0;
  background: transparent;
}

.option-content {
  flex: 1;
  min-width: 0;
}

.option-text {
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text-primary);
  margin-bottom: 0.25rem;
}

.option-description {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  line-height: 1.4;
}

.option-votes {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  min-width: 60px;
}

.vote-count {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.vote-percentage {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.user-vote-indicator {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 20px;
  height: 20px;
  background: var(--color-primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
}

.voting-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.stat-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 0.25rem;
}

.voting-actions {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  flex-wrap: wrap;
}

/* Responsive design */
@media (max-width: 640px) {
  .voting-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .voting-status {
    align-self: flex-end;
  }
  
  .voting-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .voting-option {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .option-votes {
    align-self: flex-end;
    flex-direction: row;
    gap: 1rem;
  }
  
  .voting-stats {
    grid-template-columns: 1fr;
  }
  
  .voting-actions {
    flex-direction: column;
  }
}
</style>
