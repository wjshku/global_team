<!-- MemberCard.vue - Component for displaying team member information -->
<template>
  <BaseCard 
    :class="cardClasses"
    :clickable="clickable"
    @click="handleCardClick"
  >
    <!-- Member Header -->
    <template #header>
      <div class="member-header">
        <div class="member-avatar">
          {{ getInitials(member.name) }}
        </div>
        <div class="member-info">
          <h3 class="member-name">{{ member.name || 'Unknown Member' }}</h3>
          <div class="member-role" v-if="member.role">
            {{ member.role }}
          </div>
        </div>
        <div class="member-status" v-if="showStatus">
          <div class="status-indicator" :class="statusClass"></div>
          <span class="status-text">{{ statusText }}</span>
        </div>
      </div>
    </template>

    <!-- Member Content -->
    <div class="member-content">
      <!-- Member Details -->
      <div class="member-details">
        <div class="detail-row" v-if="member.email">
          <span class="detail-icon">📧</span>
          <div class="detail-content">
            <div class="detail-label">Email</div>
            <div class="detail-value">{{ member.email }}</div>
          </div>
        </div>

        <div class="detail-row" v-if="member.timezone">
          <span class="detail-icon">🌍</span>
          <div class="detail-content">
            <div class="detail-label">Timezone</div>
            <div class="detail-value">{{ member.timezone }}</div>
          </div>
        </div>

        <div class="detail-row" v-if="showJoined && member.joinedAt">
          <span class="detail-icon">📅</span>
          <div class="detail-content">
            <div class="detail-label">Joined</div>
            <div class="detail-value">{{ formatDate(member.joinedAt) }}</div>
          </div>
        </div>

        <div class="detail-row" v-if="showBio && member.bio">
          <span class="detail-icon">📝</span>
          <div class="detail-content">
            <div class="detail-label">Bio</div>
            <div class="detail-value">{{ truncateText(member.bio, 120) }}</div>
          </div>
        </div>

        <div class="detail-row" v-if="showTeamCount && Array.isArray(member.teams)">
          <span class="detail-icon">👥</span>
          <div class="detail-content">
            <div class="detail-label">Teams</div>
            <div class="detail-value">{{ member.teams.length }} team{{ member.teams.length === 1 ? '' : 's' }}</div>
          </div>
        </div>
      </div>

      <!-- Availability Status -->
      <div v-if="showAvailability && member.availability" class="availability-section">
        <div class="availability-header">
          <span class="availability-icon">⏰</span>
          <span class="availability-label">Availability</span>
        </div>
        <div class="availability-status">
          <div class="availability-indicator" :class="availabilityClass"></div>
          <span class="availability-text">{{ availabilityText }}</span>
        </div>
      </div>

      <!-- Member Actions -->
      <div v-if="showActions" class="member-actions">
        <BaseButton
          v-if="canMessage"
          variant="secondary"
          size="small"
          @click.stop="handleMessage"
        >
          Message
        </BaseButton>
        <BaseButton
          v-if="canViewProfile"
          variant="secondary"
          size="small"
          @click.stop="handleViewProfile"
        >
          View Profile
        </BaseButton>
        <BaseButton
          v-if="canRemove"
          variant="danger"
          size="small"
          @click.stop="handleRemove"
        >
          Remove
        </BaseButton>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed } from 'vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { formatDate, truncateText } from '@/utils/formatters'

// Props definition
const props = defineProps({
  member: {
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
  showAvailability: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  showJoined: {
    type: Boolean,
    default: true
  },
  showBio: {
    type: Boolean,
    default: true
  },
  showTeamCount: {
    type: Boolean,
    default: false
  },
  canMessage: {
    type: Boolean,
    default: true
  },
  canViewProfile: {
    type: Boolean,
    default: true
  },
  canRemove: {
    type: Boolean,
    default: false
  }
})

// Emits definition
const emit = defineEmits(['click', 'message', 'view-profile', 'remove'])

// Computed properties
const cardClasses = computed(() => {
  const classes = ['member-card']
  
  if (props.clickable) {
    classes.push('member-card--clickable')
  }
  
  return classes
})

const statusClass = computed(() => {
  const status = props.member.status || 'offline'
  return `status-indicator--${status}`
})

const statusText = computed(() => {
  const status = props.member.status || 'offline'
  const statusMap = {
    online: 'Online',
    away: 'Away',
    busy: 'Busy',
    offline: 'Offline'
  }
  return statusMap[status] || 'Offline'
})

const availabilityClass = computed(() => {
  const availability = props.member.availability || 'unknown'
  return `availability-indicator--${availability}`
})

const availabilityText = computed(() => {
  const availability = props.member.availability || 'unknown'
  const availabilityMap = {
    available: 'Available',
    busy: 'Busy',
    away: 'Away',
    unavailable: 'Unavailable',
    unknown: 'Unknown'
  }
  return availabilityMap[availability] || 'Unknown'
})

// Methods
const handleCardClick = (event) => {
  console.log('MemberCard: Card clicked', props.member)
  emit('click', props.member)
}

const handleMessage = (event) => {
  console.log('MemberCard: Message clicked', props.member)
  emit('message', props.member)
}

const handleViewProfile = (event) => {
  console.log('MemberCard: View profile clicked', props.member)
  emit('view-profile', props.member)
}

const handleRemove = (event) => {
  console.log('MemberCard: Remove clicked', props.member)
  emit('remove', props.member)
}

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
.member-card {
  transition: all 0.2s ease;
}

.member-card--clickable {
  cursor: pointer;
}

.member-card--clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.member-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.member-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 600;
  flex-shrink: 0;
}

.member-info {
  flex: 1;
  min-width: 0;
}

.member-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 0.25rem 0;
  line-height: 1.3;
}

.member-role {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.member-status {
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

.status-indicator--online {
  background: #10b981;
}

.status-indicator--away {
  background: #f59e0b;
}

.status-indicator--busy {
  background: #ef4444;
}

.status-indicator--offline {
  background: #6b7280;
}

.status-text {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.member-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.member-details {
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
  font-size: 1rem;
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
  font-size: 0.9rem;
  color: var(--color-text-primary);
  line-height: 1.4;
  word-break: break-word;
}

.availability-section {
  border-top: 1px solid var(--color-border);
  padding-top: 1rem;
}

.availability-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.availability-icon {
  font-size: 1rem;
}

.availability-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.availability-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.availability-indicator--available {
  background: #10b981;
}

.availability-indicator--busy {
  background: #ef4444;
}

.availability-indicator--away {
  background: #f59e0b;
}

.availability-indicator--unavailable {
  background: #6b7280;
}

.availability-indicator--unknown {
  background: #9ca3af;
}

.availability-text {
  font-size: 0.9rem;
  color: var(--color-text-primary);
  font-weight: 500;
}

.member-actions {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  flex-wrap: wrap;
}

/* Responsive design */
@media (max-width: 640px) {
  .member-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .member-status {
    align-self: flex-end;
  }
  
  .member-actions {
    flex-direction: column;
  }
  
  .member-avatar {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}
</style>
