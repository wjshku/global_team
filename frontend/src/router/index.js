import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import PersonalView from '../views/PersonalView.vue'
import TeamView from '../views/TeamView.vue'
import MeetingView from '../views/MeetingView.vue'
import AllTeamsView from '../views/AllTeamsView.vue'
import AllMembersView from '../views/AllMembersView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import { useAuthStore } from '@/store/modules/auth'
import { useTeamsStore } from '@/store/modules/teams'
import CreateMeetingView from '../views/CreateMeetingView.vue'
import CreateTeamView from '../views/CreateTeamView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Home' }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView,
    meta: { title: 'Sign Up' }
  },
  {
    path: '/personal',
    name: 'personal',
    component: PersonalView,
    meta: { title: 'Personal Dashboard', requiresAuth: true }
  },
  {
    path: '/members',
    name: 'members',
    component: AllMembersView,
    meta: { title: 'Members', requiresAuth: true }
  },
  {
    path: '/teams',
    name: 'teams',
    component: TeamView,
    meta: { title: 'Teams', requiresAuth: true }
  },
  {
    path: '/teams/all',
    name: 'teams-all',
    component: AllTeamsView,
    meta: { title: 'All Teams', requiresAuth: true }
  },
  {
    path: '/teams/new',
    name: 'team-create',
    component: CreateTeamView,
    meta: { title: 'Create Team', requiresAuth: true }
  },
  {
    path: '/meetings',
    name: 'meetings',
    component: MeetingView,
    meta: { title: 'Meetings', requiresAuth: true }
  },
  {
    path: '/team/:id',
    name: 'team',
    component: TeamView,
    meta: { title: 'Team View', requiresAuth: true },
    props: true
  },
  {
    path: '/member/:id',
    name: 'personal-member',
    component: PersonalView,
    meta: { title: 'Personal View', requiresAuth: true },
    props: true
  },
  {
    path: '/meeting/:id',
    name: 'meeting',
    component: MeetingView,
    meta: { title: 'Meeting View', requiresAuth: true },
    props: true
  },
  {
    path: '/meetings/new',
    name: 'meeting-create',
    component: CreateMeetingView,
    meta: { title: 'Create Meeting', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: { title: 'Page Not Found' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  console.debug('[Router.beforeEach] nav start', {
    from: { path: from.path, name: from.name },
    to: { path: to.path, name: to.name, fullPath: to.fullPath, meta: to.meta }
  })
  // Set page title
  document.title = to.meta.title ? `${to.meta.title} - Global Team` : 'Global Team'
  
  // Check authentication for protected routes
  if (!to.meta.requiresAuth) {
    console.debug('[Router.beforeEach] route does not require auth, proceeding')
    return next()
  }

  const auth = useAuthStore()
  if (!auth.isLoggedIn) {
    console.debug('[Router.beforeEach] blocked: requiresAuth but user not logged in, redirecting to home')
    return next({ name: 'home' })
  }

  // Redirect generic personal route to the logged-in user's personal route
  if (to.name === 'personal') {
    const uid = auth.currentUser?.id
    if (uid) return next({ name: 'personal-member', params: { id: String(uid) } })
  }

  // Team membership guard: only allow /team/:id if user is a member
  if (to.name === 'team' && to.params.id) {
    const teamsStore = useTeamsStore()
    if (!teamsStore.allTeams.length) await teamsStore.fetchTeams()
    const uid = auth.currentUser?.id
    const team = teamsStore.getTeamById(to.params.id)
    const isMember = team && Array.isArray(team.members) && uid && team.members.includes(uid)
    if (!isMember) {
      console.debug('[Router.beforeEach] blocked: user is not a member of team, redirecting to teams-all', {
        teamId: to.params.id,
        uid,
        team
      })
      return next({ name: 'teams-all' })
    }
  }

  console.debug('[Router.beforeEach] nav allowed')
  next()
})

export default router