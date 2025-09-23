<template>
  <div class="all-members-view">
    <div class="header">
      <h1 class="title">All Members</h1>
      <input
        v-model="query"
        type="text"
        class="search-input"
        placeholder="Search members by name..."
        :disabled="isLoading"
      />
    </div>

    <div v-if="isLoading" class="loading">Loading members...</div>
    <div v-else-if="filteredMembers.length === 0" class="empty">No members found.</div>
    <div v-else class="cards">
      <MemberCard
        v-for="member in filteredMembers"
        :key="member.id"
        :member="member"
        :clickable="true"
        :show-actions="false"
        :show-availability="false"
        :show-joined="false"
        :show-bio="false"
        :show-team-count="true"
        @click="handleMemberClick(member)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MemberCard from '@/components/features/MemberCard.vue'
import { useMembersStore } from '@/store/modules/members'
import { useTeamsStore } from '@/store/modules/teams'

const router = useRouter()
const membersStore = useMembersStore()
const teamsStore = useTeamsStore()

const query = ref('')

onMounted(async () => {
  if (!membersStore.allMembers.length) await membersStore.fetchMembers()
  if (!teamsStore.allTeams.length) await teamsStore.fetchTeams()
})

const isLoading = computed(() => membersStore.isLoading)
const members = computed(() => membersStore.allMembers)

const membersWithTeams = computed(() => {
  const teamMap = new Map(teamsStore.allTeams.map(t => [t.id, t]))
  return members.value.map(m => {
    // Fallback: if m.teams is empty, infer from teamsStore membership arrays
    let teamIds = Array.isArray(m.teams) && m.teams.length > 0
      ? m.teams
      : teamsStore.allTeams.filter(t => Array.isArray(t.members) && t.members.includes(m.id)).map(t => t.id)

    const teamNames = (teamIds || []).map(tid => teamMap.get(tid)?.name).filter(Boolean)
    return { ...m, teams: teamIds, teamsResolved: teamNames }
  })
})

const filteredMembers = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return membersWithTeams.value
  return membersWithTeams.value.filter(m => (m.name || '').toLowerCase().includes(q))
})

const handleMemberClick = (member) => {
  router.push({ name: 'personal-member', params: { id: member.id } })
}
</script>

<style scoped>
.all-members-view { display: flex; flex-direction: column; gap: 16px; }
.header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.title { margin: 0; font-size: 1.5rem; font-weight: 700; }
.search-input { flex: 1; max-width: 420px; padding: 10px 12px; border-radius: 10px; border: 1px solid #e2e8f0; }
.loading, .empty { color: var(--color-text-secondary); }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }
</style>


