<!-- TeamCard.vue - Component for displaying team information -->
<template>
  <BaseCard 
    :class="cardClasses"
    :clickable="clickable"
    @click="handleCardClick"
  >
    <!-- Team Header -->
    <template #header>
      <div class="team-header">
        <div class="team-icon">
          🏢
        </div>
        <div class="team-info">
          <h3 class="team-name">{{ team.name || 'Untitled Team' }}</h3>
          <div class="team-meta">
            <span class="member-count">{{ memberCount }} members</span>
            <span v-if="team.timezone" class="team-timezone">{{ team.timezone }}</span>
          </div>
        </div>
        <div class="team-actions" v-if="showActions">
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

    <!-- Team Content -->
    <div class="team-content">
      <!-- Team Description -->
      <div v-if="team.description" class="team-description">
        <p>{{ truncateText(team.description, 150) }}</p>
      </div>

      <!-- Team Stats -->
      <div class="team-stats">
        <div class="stat-item">
          <span class="stat-icon">👥</span>
          <div class="stat-content">
            <div class="stat-value">{{ memberCount }}</div>
            <div class="stat-label">Members</div>
          </div>
        </div>
        <div class="stat-item" v-if="team.meetingCount !== undefined">
          <span class="stat-icon">📅</span>
          <div class="stat-content">
            <div class="stat-value">{{ team.meetingCount }}</div>
            <div class="stat-label">Meetings</div>
          </div>
        </div>
        <div class="stat-item" v-if="team.createdAt">
          <span class="stat-icon">📅</span>
          <div class="stat-content">
            <div class="stat-value">{{ formatDate(team.createdAt) }}</div>
            <div class="stat-label">Created</div>
          </div>
        </div>
      </div>

      <!-- Team Members Preview -->
      <div v-if="showMembersPreview && teamMembers.length > 0" class="members-preview">
        <div class="members-header">
          <span class="members-icon">👥</span>
          <span class="members-label">Team Members</span>
        </div>
        <div class="members-list">
          <div 
            v-for="member in teamMembers.slice(0, maxVisibleMembers)" 
            :key="member.id || member"
            class="member-item"
          >
            <div class="member-avatar">
              {{ getInitials(member.name || member) }}
            </div>
            <span class="member-name">{{ member.name || member }}</span>
          </div>
          <div v-if="teamMembers.length > maxVisibleMembers" class="member-more">
            +{{ teamMembers.length - maxVisibleMembers }} more
          </div>
        </div>
      </div>

      <!-- Team Actions -->
      <div v-if="showTeamActions" class="team-actions-footer">
        <BaseButton
          variant="primary"
          size="small"
          @click="handleJoin"
          :disabled="!canJoin"
        >
          {{ joinButtonText }}
        </BaseButton>
        <BaseButton
          v-if="canLeave"
          variant="secondary"
          size="small"
          @click="handleLeave"
        >
          Leave Team
        </BaseButton>
        <BaseButton
          v-if="canViewDetails"
          variant="secondary"
          size="small"
          @click="handleViewDetails"
        >
          View Details
        </BaseButton>
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import { formatDate, truncateText } from '@/utils/formatters'
import { useMembersStore } from '@/store'

// Props definition
const props = defineProps({
  team: {
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
  showMembersPreview: {
    type: Boolean,
    default: true
  },
  showTeamActions: {
    type: Boolean,
    default: true
  },
  maxVisibleMembers: {
    type: Number,
    default: 4
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
  canLeave: {
    type: Boolean,
    default: false
  },
  canViewDetails: {
    type: Boolean,
    default: true
  },
  isJoined: {
    type: Boolean,
    default: false
  }
})

// Emits definition
const emit = defineEmits(['click', 'edit', 'delete', 'join', 'leave', 'view-details'])

// Computed properties
const cardClasses = computed(() => {
  const classes = ['team-card']
  
  if (props.clickable) {
    classes.push('team-card--clickable')
  }
  
  if (props.isJoined) {
    classes.push('team-card--joined')
  }
  
  return classes
})

// Members store for resolving member IDs to member objects
const membersStore = useMembersStore()

// Ensure members are loaded so IDs can be resolved to names
onMounted(() => {
  if (!membersStore.allMembers || membersStore.allMembers.length === 0) {
    // Fire-and-forget; errors are handled in the store
    membersStore.fetchMembers()
  }
})

const memberCount = computed(() => {
  if (props.team.memberCount !== undefined) {
    return props.team.memberCount
  }
  return teamMembers.value.length
})

const teamMembers = computed(() => {
  if (!props.team.members || !Array.isArray(props.team.members)) return []

  // Normalize to array of member objects with id and name
  return props.team.members
    .map((entry) => {
      // If already an object with a name, return as is
      if (entry && typeof entry === 'object') {
        return entry
      }
      // Otherwise treat as an ID and resolve via store
      const resolved = membersStore.getMemberById?.(entry)
      if (resolved) return resolved
      // Fallback object if not found yet
      return { id: entry, name: String(entry) }
    })
    .filter(Boolean)
})

const joinButtonText = computed(() => {
  if (props.isJoined) {
    return 'Joined'
  }
  return 'Join Team'
})

// Methods
const handleCardClick = (event) => {
  console.log('TeamCard: Card clicked', props.team)
  emit('click', props.team)
}

const handleEdit = (event) => {
  console.log('TeamCard: Edit clicked', props.team)
  emit('edit', props.team)
}

const handleDelete = (event) => {
  console.log('TeamCard: Delete clicked', props.team)
  emit('delete', props.team)
}

const handleJoin = (event) => {
  console.log('TeamCard: Join clicked', props.team)
  emit('join', props.team)
}

const handleLeave = (event) => {
  console.log('TeamCard: Leave clicked', props.team)
  emit('leave', props.team)
}

const handleViewDetails = (event) => {
  console.log('TeamCard: View details clicked', props.team)
  emit('view-details', props.team)
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
.team-card {
  transition: all 0.2s ease;
}

.team-card--clickable {
  cursor: pointer;
}

.team-card--clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.team-card--joined {
  border-left: 4px solid var(--color-primary);
}

.team-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.team-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.team-info {
  flex: 1;
  min-width: 0;
}

.team-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
}

.team-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.member-count {
  font-weight: 500;
}

.team-timezone {
  background: var(--bg-tertiary);
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-secondary);
  border: 1px solid var(--border-primary);
}

.team-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.team-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.team-description {
  color: var(--text-primary);
  line-height: 1.6;
}

.team-description p {
  margin: 0;
}

.team-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--border-primary);
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
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 0.25rem;
}

.members-preview {
  border-top: 1px solid var(--border-primary);
  padding-top: 1rem;
}

.members-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.members-icon {
  font-size: 1rem;
}

.members-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: var(--bg-tertiary);
  border-radius: 16px;
  font-size: 0.8rem;
}

.member-avatar {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 600;
}

.member-name {
  color: var(--text-primary);
  font-weight: 500;
}

.member-more {
  display: flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: var(--bg-tertiary);
  border-radius: 16px;
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Removed OS-level dark overrides; rely on CSS variables for theming */

.team-actions-footer {
  display: flex;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-primary);
  flex-wrap: wrap;
}

/* Responsive design */
@media (max-width: 640px) {
  .team-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .team-actions {
    align-self: flex-end;
  }
  
  .team-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .team-stats {
    grid-template-columns: 1fr;
  }
  
  .team-actions-footer {
    flex-direction: column;
  }
  
  .members-list {
    flex-direction: column;
  }
  
  .member-item {
    justify-content: flex-start;
  }
}
</style>
