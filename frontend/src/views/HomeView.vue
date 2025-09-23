<template>
  <div class="home-view">
    <!-- Welcome Section -->
    <section class="welcome-section">
      <h1 class="welcome-title">
        <span class="welcome-icon">🌍</span>
        Global Team Manager
      </h1>
      <p class="welcome-description">
        Coordinate your distributed team across different timezones and schedule meetings efficiently.
      </p>
    </section>

    <!-- Authentication Section -->
    <section v-if="!isLoggedIn" class="auth-section">
      <div class="auth-cards">
        <LoginCard @login-success="handleLoginSuccess" />
        <SignupCard @signup-success="handleSignupSuccess" />
      </div>
    </section>

    <!-- Main Content - Only visible when logged in -->
    <section v-if="isLoggedIn" class="main-content">
      <div class="content-grid">
        <!-- Members Card -->
        <BaseCard class="content-card">
          <template #header>
            <h3 class="card-title">
              <span class="card-icon">👥</span>
              Members
            </h3>
          </template>
          <!-- Remove #content wrapper - put content directly here -->
          <div class="card-content">
            <p class="card-description">Manage team members and their timezones</p>
            <div class="card-stats">
              <span class="stat-item">
                <strong>{{ memberCount }}</strong> members
              </span>
            </div>
            <BaseButton 
              @click="navigateToMembers" 
              variant="primary"
              class="card-action"
            >
              View Members
            </BaseButton>
          </div>
        </BaseCard>

        <!-- Teams Card -->
        <BaseCard class="content-card">
          <template #header>
            <h3 class="card-title">
              <span class="card-icon">🏢</span>
              Teams
            </h3>
          </template>
          <!-- Remove #content wrapper - put content directly here -->
          <div class="card-content">
            <p class="card-description">Create and manage teams</p>
            <div class="card-stats">
              <span class="stat-item">
                <strong>{{ teamCount }}</strong> teams
              </span>
            </div>
            <BaseButton 
              @click="navigateToTeams" 
              variant="primary"
              class="card-action"
            >
              View Teams
            </BaseButton>
          </div>
        </BaseCard>

        <!-- Meetings Card -->
        <BaseCard class="content-card">
          <template #header>
            <h3 class="card-title">
              <span class="card-icon">📅</span>
              Meetings
            </h3>
          </template>
          <!-- Remove #content wrapper - put content directly here -->
          <div class="card-content">
            <p class="card-description">Schedule and manage meetings</p>
            <div class="card-stats">
              <span class="stat-item">
                <strong>{{ meetingCount }}</strong> meetings
              </span>
            </div>
            <BaseButton 
              @click="navigateToMeetings" 
              variant="primary"
              class="card-action"
            >
              View Meetings
            </BaseButton>
          </div>
        </BaseCard>
      </div>
    </section>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p class="loading-text">Loading...</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'
import { useMembersStore } from '@/store/modules/members'
import { useTeamsStore } from '@/store/modules/teams'
import { useMeetingsStore } from '@/store/modules/meetings'
import { useUIStore } from '@/store/modules/ui'
import BaseCard from '@/components/common/BaseCard.vue'
import BaseButton from '@/components/common/BaseButton.vue'
import LoginCard from '@/components/features/LoginCard.vue'
import SignupCard from '@/components/features/SignupCard.vue'

export default {
  name: 'HomeView',
  components: {
    BaseCard,
    BaseButton,
    LoginCard,
    SignupCard
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const membersStore = useMembersStore()
    const teamsStore = useTeamsStore()
    const meetingsStore = useMeetingsStore()
    const uiStore = useUIStore()
    
    // Reactive data
    const isLoading = ref(false)
    
    // Computed properties
    const isLoggedIn = computed(() => {
      console.log('HomeView: Checking login status', authStore.isLoggedIn)
      return authStore.isLoggedIn
    })
    
    const memberCount = computed(() => {
      const count = membersStore.allMembers.length
      console.log('HomeView: Member count', count)
      return count
    })
    
    const teamCount = computed(() => {
      const count = teamsStore.allTeams.length
      console.log('HomeView: Team count', count)
      return count
    })
    
    const meetingCount = computed(() => {
      const count = meetingsStore.meetingCount
      console.log('HomeView: Meeting count', count)
      return count
    })
    
    // Methods
    const handleLoginSuccess = (userData) => {
      console.log('HomeView: Login successful', userData)
      // Store will be updated by the LoginCard component
      // Force reactivity update
      authStore.login(userData)
    }
    
    const handleSignupSuccess = (userData) => {
      console.log('HomeView: Signup successful', userData)
      // Store will be updated by the SignupCard component
      authStore.login(userData)
    }
    
    const navigateToMembers = () => {
      console.log('HomeView: Navigating to members')
      router.push('/members')
    }
    
    const navigateToTeams = () => {
      console.log('HomeView: Navigating to teams')
      router.push({ name: 'teams-all' })
    }
    
    const navigateToMeetings = () => {
      console.log('HomeView: Navigating to meetings')
      router.push('/meetings')
    }
    
    const loadInitialData = async () => {
      if (isLoggedIn.value) {
        console.log('HomeView: Loading initial data for logged-in user')
        isLoading.value = true
        
        try {
          // Load user's data in parallel
          await Promise.all([
            membersStore.fetchMembers(),
            teamsStore.fetchTeams(),
            meetingsStore.fetchMeetings()
          ])
          console.log('HomeView: Initial data loaded successfully')
        } catch (error) {
          console.error('HomeView: Error loading initial data', error)
          // Handle error gracefully - show user-friendly message
          uiStore.showNotification({
            type: 'error',
            message: 'Failed to load some data. Please refresh the page.'
          })
        } finally {
          isLoading.value = false
        }
      }
    }
    
    // Lifecycle
    onMounted(() => {
      console.log('HomeView: Component mounted')
      loadInitialData()
    })
    
    return {
      // Reactive data
      isLoading,
      
      // Computed properties
      isLoggedIn,
      memberCount,
      teamCount,
      meetingCount,
      
      // Methods
      handleLoginSuccess,
      handleSignupSuccess,
      navigateToMembers,
      navigateToTeams,
      navigateToMeetings
    }
  }
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  padding: 2rem 0;
}

.welcome-section {
  text-align: center;
  margin-bottom: 3rem;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.welcome-icon {
  font-size: 3rem;
}

.welcome-description {
  font-size: 1.2rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.auth-section {
  margin-bottom: 3rem;
}

.auth-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.content-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.content-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-icon {
  font-size: 1.5rem;
}

.card-content {
  text-align: center;
}

.card-description {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.card-stats {
  margin-bottom: 1.5rem;
}

.stat-item {
  display: block;
  font-size: 1.1rem;
  color: var(--text-primary);
}

.card-action {
  width: 100%;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-primary);
  border-top: 4px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-text {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive design */
@media (max-width: 768px) {
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-icon {
    font-size: 2.5rem;
  }
  
  .welcome-description {
    font-size: 1.1rem;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .auth-cards {
    grid-template-columns: 1fr;
  }
}
</style>
