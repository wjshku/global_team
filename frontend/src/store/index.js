import { createPinia } from 'pinia'
import { useAuthStore } from './modules/auth'
import { useTeamsStore } from './modules/teams'
import { useMembersStore } from './modules/members'
import { useMeetingsStore } from './modules/meetings'
import { useUIStore } from './modules/ui'

// Create Pinia instance
const pinia = createPinia()

// Export stores for easy access
export {
  useAuthStore,
  useTeamsStore,
  useMembersStore,
  useMeetingsStore,
  useUIStore
}

export default pinia