<template>
  <div class="all-teams-view">
    <div class="header">
      <h1 class="title">All Teams</h1>
      <input
        v-model="query"
        type="text"
        class="search-input"
        placeholder="Search teams by name..."
        :disabled="isLoading"
      />
      <BaseButton @click="goToCreate" :disabled="isLoading">Create Team</BaseButton>
    </div>

    <div v-if="isLoading" class="loading">Loading teams...</div>
    <div v-else-if="filteredTeams.length === 0" class="empty">No teams found.</div>
    <div v-else class="cards">
      <TeamCard
        v-for="team in filteredTeams"
        :key="team.id"
        :team="team"
        :clickable="true"
        :show-actions="false"
        :show-members-preview="true"
        :show-team-actions="false"
        :is-joined="userTeamIds.has(team.id)"
        @click="handleTeamClick(team)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/common/BaseButton.vue'
import TeamCard from '@/components/features/TeamCard.vue'
import { useTeamsStore } from '@/store/modules/teams'
import { useMembersStore } from '@/store/modules/members'
import { useAuthStore } from '@/store/modules/auth'

const router = useRouter()
const teamsStore = useTeamsStore()
const membersStore = useMembersStore()
const authStore = useAuthStore()

const query = ref('')

onMounted(async () => {
  if (!teamsStore.allTeams.length) await teamsStore.fetchTeams()
  if (!membersStore.allMembers.length) await membersStore.fetchMembers()
})

const isLoading = computed(() => teamsStore.isLoading)
const teams = computed(() => teamsStore.allTeams)

const userId = computed(() => authStore.currentUser?.id || membersStore.currentMember?.id || null)
const userTeamIds = computed(() => {
  const set = new Set()
  const uid = userId.value
  if (!uid) return set
  teams.value.forEach(t => { if (Array.isArray(t.members) && t.members.includes(uid)) set.add(t.id) })
  return set
})

const filteredTeams = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return teams.value
  return teams.value.filter(t => (t.name || '').toLowerCase().includes(q))
})

const handleTeamClick = (team) => {
  if (userTeamIds.value.has(team.id)) {
    router.push({ name: 'team', params: { id: team.id } })
  } else {
    console.warn('Access denied: user is not a member of this team')
  }
}

const goToCreate = () => {
  router.push({ name: 'team-create' })
}
</script>

<style scoped>
.all-teams-view { display: flex; flex-direction: column; gap: 16px; }
.header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.title { margin: 0; font-size: 1.5rem; font-weight: 700; }
.search-input { flex: 1; max-width: 420px; padding: 10px 12px; border-radius: 10px; border: 1px solid #e2e8f0; }
.loading, .empty { color: var(--color-text-secondary); }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }
</style>


