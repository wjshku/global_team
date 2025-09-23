<!-- MeetingCard.vue - Component for displaying meeting information -->
<template>
  <BaseCard 
    :class="cardClasses"
    :clickable="clickable"
    @click="handleCardClick"
  >
    <!-- Meeting Header -->
    <template #header>
      <div class="meeting-header">
        <div class="meeting-title">
          <h3 class="meeting-name">{{ meeting.title || 'Untitled Meeting' }}</h3>
          <div class="meeting-status" :class="statusClass">
            {{ statusText }}
          </div>
        </div>
        <div class="meeting-actions" v-if="showActions">
          <BaseButton
            v-if="canEdit"
            variant="secondary"
            size="small"
            @click.stop="handleEdit"
          >
            Edit
          </BaseButton>
          <BaseButton
            v-if="canDelete"
            variant="danger"
            size="small"
            @click.stop="handleDelete"
          >
            Delete
          </BaseButton>
        </div>
      </div>
    </template>

    <!-- Meeting Content -->
    <div class="meeting-content">
      <!-- Meeting Details -->
      <div class="meeting-details">
        <div class="detail-row">
          <span class="detail-icon">📅</span>
          <div class="detail-content">
            <div class="detail-label">Date & Time</div>
            <div class="detail-value">{{ formatDateTime(meeting.scheduledTime || meeting.startTime, { timeZone: userTz }) }}</div>
            <div v-if="meeting.endTime" class="detail-sublabel">
              Duration: {{ formatDuration(new Date(meeting.endTime) - new Date(meeting.startTime)) }}
            </div>
          </div>
        </div>

        <div class="detail-row" v-if="meeting.location">
          <span class="detail-icon">📍</span>
          <div class="detail-content">
            <div class="detail-label">Location</div>
            <div class="detail-value">{{ meeting.location }}</div>
          </div>
        </div>

        <div class="detail-row" v-if="meeting.description">
          <span class="detail-icon">📝</span>
          <div class="detail-content">
            <div class="detail-label">Description</div>
            <div class="detail-value">{{ truncateText(meeting.description, 100) }}</div>
          </div>
        </div>

        <div class="detail-row" v-if="meeting.organizer">
          <span class="detail-icon">👤</span>
          <div class="detail-content">
            <div class="detail-label">Organizer</div>
            <div class="detail-value">{{ meeting.organizer.name || meeting.organizer }}</div>
          </div>
        </div>
      </div>

      <!-- Team Context (if showTeamContext is true) -->
      <div v-if="showTeamContext && meeting.team" class="team-context">
        <div class="team-info">
          <span class="team-icon">🏢</span>
          <span class="team-name">{{ meeting.team.name }}</span>
        </div>
      </div>

      <!-- Attendees List -->
      <div v-if="meeting.attendees && meeting.attendees.length > 0" class="attendees-section">
        <div class="attendees-header">
          <span class="attendees-icon">👥</span>
          <span class="attendees-label">Attendees ({{ meeting.attendees.length }})</span>
        </div>
        <div class="attendees-list">
          <div 
            v-for="attendee in meeting.attendees.slice(0, maxVisibleAttendees)" 
            :key="attendee.id || attendee"
            class="attendee-item"
          >
            <div class="attendee-avatar">
              {{ getInitials(attendee.name || attendee) }}
            </div>
            <span class="attendee-name">{{ attendee.name || attendee }}</span>
          </div>
          <div v-if="meeting.attendees.length > maxVisibleAttendees" class="attendee-more">
            +{{ meeting.attendees.length - maxVisibleAttendees }} more
          </div>
        </div>
      </div>

      <!-- Meeting Actions -->
      <div v-if="showMeetingActions" class="meeting-actions-footer">
        <BaseButton
          variant="primary"
          size="small"
          @click="handleJoin"
          :disabled="!canJoin"
        >
          {{ joinButtonText }}
        </BaseButton>
        <BaseButton
          v-if="canVote"
          variant="secondary"
          size="small"
          @click="handleVote"
        >
          Vote on Time
        </BaseButton>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { formatDate, formatTime, formatDateTime, formatDuration, truncateText } from '@/utils/formatters'
import { MEETING_STATUS, UI_CONSTANTS } from '@/utils/constants'

// Props definition
const props = defineProps({
  meeting: {
    type: Object,
    required: true,
    default: () => ({})
  },
  clickable: {
    type: Boolean,
    default: false
  },
  showActions: {
    type: Boolean,
    default: true
  },
  showTeamContext: {
    type: Boolean,
    default: false
  },
  showMeetingActions: {
    type: Boolean,
    default: true
  },
  maxVisibleAttendees: {
    type: Number,
    default: 5
  },
  canEdit: {
    type: Boolean,
    default: false
  },
  canDelete: {
    type: Boolean,
    default: false
  },
  canJoin: {
    type: Boolean,
    default: true
  },
  canVote: {
    type: Boolean,
    default: false
  }
})

// Emits definition
const emit = defineEmits(['click', 'edit', 'delete', 'join', 'vote'])

// Computed properties
const authStore = useAuthStore()
const userTz = computed(() => authStore.currentUser?.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone)
const cardClasses = computed(() => {
  const classes = ['meeting-card']
  
  if (props.meeting.status) {
    classes.push(`meeting-card--${props.meeting.status}`)
  }
  
  if (props.clickable) {
    classes.push('meeting-card--clickable')
  }
  
  return classes
})

const statusClass = computed(() => {
  const status = props.meeting.status || 'scheduled'
  return `meeting-status--${status}`
})

const statusText = computed(() => {
  const status = props.meeting.status || MEETING_STATUS.SCHEDULED
  const statusMap = {
    [MEETING_STATUS.SCHEDULED]: 'Scheduled',
    [MEETING_STATUS.IN_PROGRESS]: 'In Progress',
    [MEETING_STATUS.COMPLETED]: 'Completed',
    [MEETING_STATUS.CANCELLED]: 'Cancelled',
    draft: 'Draft'
  }
  return statusMap[status] || 'Scheduled'
})

const joinButtonText = computed(() => {
  const status = props.meeting.status || MEETING_STATUS.SCHEDULED
  const buttonMap = {
    [MEETING_STATUS.SCHEDULED]: 'Join Meeting',
    [MEETING_STATUS.IN_PROGRESS]: 'Join Now',
    [MEETING_STATUS.COMPLETED]: 'View Recording',
    [MEETING_STATUS.CANCELLED]: 'Cancelled',
    draft: 'Not Available'
  }
  return buttonMap[status] || 'Join Meeting'
})

// Methods
const handleCardClick = (event) => {
  console.log('MeetingCard: Card clicked', props.meeting)
  emit('click', props.meeting)
}

const handleEdit = (event) => {
  console.log('MeetingCard: Edit clicked', props.meeting)
  emit('edit', props.meeting)
}

const handleDelete = (event) => {
  console.log('MeetingCard: Delete clicked', props.meeting)
  emit('delete', props.meeting)
}

const handleJoin = (event) => {
  console.log('MeetingCard: Join clicked', props.meeting)
  emit('join', props.meeting)
}

const handleVote = (event) => {
  console.log('MeetingCard: Vote clicked', props.meeting)
  emit('vote', props.meeting)
}

// Removed custom formatDateTime and formatDuration - now using utility functions

const getInitials = (name) => {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
</script>

<style scoped>
.meeting-card {
  transition: all 0.2s ease;
}

.meeting-card--clickable {
  cursor: pointer;
}

.meeting-card--clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.meeting-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.meeting-title {
  flex: 1;
}

.meeting-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
}

.meeting-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.meeting-status--scheduled {
  background: #dbeafe;
  color: #1e40af;
}

.meeting-status--in_progress {
  background: #dcfce7;
  color: #166534;
}

.meeting-status--completed {
  background: #f3f4f6;
  color: #374151;
}

.meeting-status--cancelled {
  background: #fef2f2;
  color: #dc2626;
}

.meeting-status--draft {
  background: #fef3c7;
  color: #d97706;
}

.meeting-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.meeting-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.meeting-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-row {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.detail-icon {
  font-size: 1.1rem;
  margin-top: 0.1rem;
  flex-shrink: 0;
}

.detail-content {
  flex: 1;
  min-width: 0;
}

.detail-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.25rem;
}

.detail-value {
  font-size: 0.95rem;
  color: var(--color-text-primary);
  line-height: 1.4;
}

.detail-sublabel {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  margin-top: 0.25rem;
}

.team-context {
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.team-icon {
  font-size: 1rem;
}

.team-name {
  font-weight: 500;
}

.attendees-section {
  border-top: 1px solid var(--color-border);
  padding-top: 1rem;
}

.attendees-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.attendees-icon {
  font-size: 1rem;
}

.attendees-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.attendee-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: #f1f5f9;
  border-radius: 16px;
  font-size: 0.8rem;
}

.attendee-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 600;
}

.attendee-name {
  color: var(--color-text-primary);
  font-weight: 500;
}

.attendee-more {
  display: flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: #e2e8f0;
  border-radius: 16px;
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.meeting-actions-footer {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

/* Responsive design */
@media (max-width: 640px) {
  .meeting-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .meeting-actions {
    justify-content: flex-end;
  }
  
  .meeting-actions-footer {
    flex-direction: column;
  }
  
  .attendees-list {
    flex-direction: column;
  }
  
  .attendee-item {
    justify-content: flex-start;
  }
}
</style>
