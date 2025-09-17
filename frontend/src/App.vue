<template>
  <div class="app">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="header-content">
          <h1 class="logo">
            <span class="logo-icon">🌍</span>
            Global Team Manager
          </h1>
    <nav class="nav">
            <button @click="goHome" class="nav-link" :class="{ active: !team && !showMe }">
              <span class="nav-icon">🏠</span>
              Home
            </button>
            <button @click="openMe" class="nav-link" :class="{ active: showMe }">
              <span class="nav-icon">👤</span>
              My Space
            </button>
            <span v-if="team" class="nav-separator">/</span>
            <span v-if="team" class="nav-current">
              <span class="nav-icon">👥</span>
              {{ team }}
            </span>
    </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main">
      <div class="container">
        <!-- Home View -->
        <div v-if="!team && !showMe" class="home-view">
          <div class="welcome-section">
            <h2>Welcome to Global Team Manager</h2>
            <p>Manage your distributed team across different timezones and schedule meetings efficiently.</p>
          </div>

          <div class="grid">
            <!-- Add Member Card -->
      <div class="card">
              <div class="card-header">
                <h3>
                  <span class="card-icon">👤</span>
                  Add Team Member
                </h3>
              </div>
              <div class="card-content">
                <form @submit.prevent="addMember" class="form">
                  <div class="form-group">
                    <label for="memberName">Name</label>
                    <input 
                      id="memberName"
                      v-model.trim="memberName" 
                      type="text" 
                      required 
                      maxlength="100"
                      placeholder="Enter member name"
                      class="form-input"
                    />
                  </div>
                  <div class="form-group">
                    <label for="memberTz">Timezone</label>
                    <input v-if="timezones.length" v-model.trim="tzSearchHome" class="form-input tz-search" placeholder="Search city/timezone (e.g., Singapore, New York)" />
                    <select v-if="timezones.length" id="memberTz" v-model="memberTz" class="form-input" required>
                      <option value="" disabled>Select your timezone</option>
                      <option v-for="tz in tzOptionsHome" :key="tz" :value="tz">{{ tz }}</option>
                    </select>
                    <input v-else id="memberTz" v-model.trim="memberTz" type="text" required placeholder="e.g., Europe/London" class="form-input" />
                    <small class="form-help">Use standard timezone names (IANA)</small>
                  </div>
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <span v-if="loading" class="spinner"></span>
                    Add Member
                  </button>
        </form>
              </div>
      </div>

            <!-- Members List Card -->
      <div class="card">
              <div class="card-header">
                <h3>
                  <span class="card-icon">👥</span>
                  Team Members
                  <span class="badge">{{ members.length }}</span>
                </h3>
                <button @click="loadMembers" class="btn btn-secondary btn-sm" :disabled="loading">
                  <span class="btn-icon">🔄</span>
                  Refresh
                </button>
              </div>
              <div class="card-content">
                <div v-if="members.length === 0" class="empty-state">
                  <span class="empty-icon">👥</span>
                  <p>No members yet. Add your first team member!</p>
                </div>
                <div v-else class="members-list">
                  <div v-for="m in members" :key="m.name" class="member-item">
                    <div class="member-info">
                      <span class="member-name">{{ m.name }}</span>
                      <span class="member-timezone">{{ m.timezone }}</span>
                    </div>
                  </div>
                </div>
              </div>
      </div>

            <!-- Teams Card -->
      <div class="card">
              <div class="card-header">
                <h3>
                  <span class="card-icon">🏢</span>
                  Teams
                  <span class="badge">{{ teams.length }}</span>
                </h3>
              </div>
              <div class="card-content">
                <form @submit.prevent="createTeam" class="form">
                  <div class="form-group">
                    <label for="teamName">Team Name</label>
                    <input 
                      id="teamName"
                      v-model.trim="teamName" 
                      type="text" 
                      required 
                      maxlength="100"
                      placeholder="Enter team name"
                      class="form-input"
                    />
                  </div>
                  <div class="form-group">
                    <label for="creatorName">Your Name</label>
                    <input 
                      id="creatorName"
                      v-model.trim="creatorName" 
                      type="text" 
                      required 
                      maxlength="100"
                      placeholder="Enter your name"
                      class="form-input"
                    />
                  </div>
                  <div class="form-group">
                    <label for="creatorTz">Your Timezone</label>
                    <input v-if="timezones.length" v-model.trim="tzSearchHome" class="form-input tz-search" placeholder="Search city/timezone" />
                    <select v-if="timezones.length" id="creatorTz" v-model="creatorTz" class="form-input" required>
                      <option value="" disabled>Select your timezone</option>
                      <option v-for="tz in tzOptionsHome" :key="tz" :value="tz">{{ tz }}</option>
                    </select>
                    <input v-else id="creatorTz" v-model.trim="creatorTz" type="text" required placeholder="e.g., Europe/London" class="form-input" />
                  </div>
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <span v-if="loading" class="spinner"></span>
                    Create Team
                  </button>
        </form>

                <div v-if="teams.length === 0" class="empty-state">
                  <span class="empty-icon">🏢</span>
                  <p>No teams yet. Create your first team!</p>
      </div>
                <div v-else class="teams-list">
                  <div v-for="t in teams" :key="t.name" class="team-item" @click="openTeam(t.name)">
                    <div class="team-info">
                      <span class="team-name">{{ t.name }}</span>
                      <span class="team-count">{{ t.member_count }} member{{ t.member_count !== 1 ? 's' : '' }}</span>
                    </div>
                    <span class="team-arrow">→</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
      </div>

        <!-- My Space View -->
        <div v-else-if="showMe" class="me-view">
          <div class="team-header">
            <h2>
              <span class="team-icon">👤</span>
              My Space
            </h2>
          </div>
          <div class="card auth-card" v-if="!meName">
            <div class="card-content">
              <form @submit.prevent="loadMe" class="form">
                <div class="form-group">
                  <label for="meName">Your Name</label>
                  <input id="meName" v-model.trim="meNameInput" class="form-input" required placeholder="Enter your member name" />
                </div>
                <button type="submit" class="btn btn-primary">Enter</button>
        </form>
      </div>
        </div>
          <div v-else class="grid">
            <div class="card">
              <div class="card-header">
                <h3><span class="card-icon">🌐</span> Timezone</h3>
              </div>
              <div class="card-content">
                <form @submit.prevent="saveTimezone" class="form">
                  <div class="form-group">
                    <label for="meTz">Timezone</label>
                    <input v-if="timezones.length" v-model.trim="tzSearchMe" class="form-input tz-search" placeholder="Search city/timezone" />
                    <select v-if="timezones.length" id="meTz" v-model="meTimezone" class="form-input" required>
                      <option value="" disabled>Select your timezone</option>
                      <option v-for="tz in tzOptionsMe" :key="tz" :value="tz">{{ tz }}</option>
                    </select>
                    <input v-else id="meTz" v-model.trim="meTimezone" class="form-input" required placeholder="e.g., Europe/London" />
                  </div>
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <span v-if="loading" class="spinner"></span>
                    Save Timezone
                  </button>
          </form>
        </div>
            </div>

            <div class="card">
              <div class="card-header">
                <h3><span class="card-icon">🕒</span> Availability ({{ meDisplayTimezone || 'UTC' }})</h3>
              </div>
              <div class="card-content">
                <div class="tz-picker" style="margin-bottom:8px; gap:8px;">
                  <label style="font-size:12px;color:var(--text-secondary)">Display TZ</label>
                  <input v-if="timezones.length" v-model.trim="tzSearchMeDisplay" class="form-input tz-search" placeholder="Search city/timezone" style="min-width:220px" />
                  <select v-if="timezones.length" v-model="meDisplayTimezone" class="form-input" style="min-width:220px">
                    <option v-for="tz in tzOptionsMeDisplay" :key="tz" :value="tz">{{ tz }}</option>
                  </select>
                </div>
                <div class="availability-editor"
                     @mousedown.prevent="startDrag(false, $event)"
                     @mousemove.prevent="onDrag($event)"
                     @mouseup.prevent="endDrag"
                     @mouseleave.prevent="endDrag"
                     @touchstart.prevent="startDrag(true, $event)"
                     @touchmove.prevent="onDrag($event, true)"
                     @touchend.prevent="endDrag">
                  <button v-for="(v, i) in meAvailabilityLocal" :key="i" class="hour" :data-index="i"
                          :class="{ on: v === 1, dragging: isDragging && i === dragLast }">
                    {{ hourLabelMe(i) }}
                  </button>
                </div>
                <div class="form-help">Click hours to toggle availability. Green = available.</div>
                <button class="btn btn-primary" style="margin-top: 12px;" @click="saveAvailability" :disabled="loading">
                  <span v-if="loading" class="spinner"></span>
                  Save Availability
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Team View -->
        <div v-else class="team-view">
          <div class="team-header">
            <h2>
              <span class="team-icon">👥</span>
              {{ team }}
            </h2>
            <p v-if="!authed">Enter your name to access this team</p>
          </div>

          <!-- Authentication Form -->
          <div v-if="!authed" class="card auth-card">
            <div class="card-content">
              <form @submit.prevent="join" class="form">
                <div class="form-group">
                  <label for="requester">Your Name</label>
                  <input 
                    id="requester"
                    v-model.trim="requester" 
                    type="text" 
                    required 
                    maxlength="100"
                    placeholder="Enter your name to join the team"
                    class="form-input"
                  />
                </div>
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="spinner"></span>
                  Join Team
                </button>
          </form>
            </div>
          </div>

          <!-- Team Content -->
          <div v-else class="team-content">
            <div class="card">
              <div class="card-header">
                <h3><span class="card-icon">📊</span> Team Availability (<span>{{ displayTzLabel }}</span>)</h3>
                <div class="tz-picker">
                  <label style="font-size:12px;color:var(--text-secondary)">Display TZ</label>
                  <input v-if="timezones.length" v-model.trim="tzSearchDisplay" class="form-input tz-search" placeholder="Search city/timezone" style="min-width:220px" />
                  <select v-if="timezones.length" v-model="displayTimezone" class="form-input" style="min-width:220px">
                    <option v-for="tz in tzOptionsDisplay" :key="tz" :value="tz">{{ tz }}</option>
                  </select>
                </div>
              </div>
              <div class="card-content">
                <div class="availability-aggregate">
                  <div v-for="h in 24" :key="h" class="aggregate-hour" :style="aggregateStyleLocal(h-1)" @mouseenter="showHourTooltip(h-1, $event)" @mouseleave="hideHourTooltip" @click="toggleHourPopup(h-1, $event)">{{ hourLabel(h-1) }}</div>
                </div>
                <div class="form-help">Bar intensity shows how many members are available each hour. Hover/click to see names.</div>
              </div>
            </div>

            <!-- Hour tooltip for aggregate availability -->
            <div v-if="hourTooltip.visible" class="hour-tooltip" :style="{ left: hourTooltip.x + 'px', top: hourTooltip.y + 'px' }">
              <div style="font-weight:600; margin-bottom:6px;">Hour: {{ hourLabel(hourTooltip.hour) }} ({{ (teamAvailabilityLocal[hourTooltip.hour] || []).length }})</div>
              <div v-if="(teamAvailabilityLocal[hourTooltip.hour]||[]).length === 0" style="color: var(--text-secondary)">No one available</div>
              <ul v-else style="margin:0; padding-left:16px; max-height:160px; overflow:auto;">
                <li v-for="name in teamAvailabilityLocal[hourTooltip.hour]" :key="name">{{ name }}</li>
          </ul>
        </div>

            <div class="grid">
              <!-- Team Members -->
              <div class="card">
                <div class="card-header">
                  <h3>
                    <span class="card-icon">👥</span>
                    Team Members
                    <span class="badge">{{ teamMembers.length }}</span>
                  </h3>
                </div>
                <div class="card-content">
                  <div v-if="teamMembers.length === 0" class="empty-state">
                    <span class="empty-icon">👥</span>
                    <p>No members in this team yet.</p>
                  </div>
                  <div v-else class="members-list">
                    <div v-for="m in teamMembers" :key="m.name" class="member-item">
                      <div class="member-info">
                        <span class="member-name">{{ m.name }}</span>
                        <span class="member-timezone">{{ m.timezone }}</span>
                      </div>
                      <div class="availability-bar">
                        <span v-for="(v,i) in (m.availability || empty24)" :key="i" class="cell" :class="{ on: v === 1 }"></span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Add Member to Team -->
              <div class="card">
                <div class="card-header">
                  <h3>
                    <span class="card-icon">➕</span>
                    Add Member to Team
                  </h3>
                </div>
                <div class="card-content">
                  <form @submit.prevent="addToTeam" class="form">
                    <div class="form-group">
                      <label for="newTeamMember">Member Name</label>
                      <input 
                        id="newTeamMember"
                        v-model.trim="newTeamMember" 
                        type="text" 
                        required 
                        maxlength="100"
                        placeholder="Enter member name"
                        class="form-input"
                      />
                    </div>
                    <button type="submit" class="btn btn-primary" :disabled="loading">
                      <span v-if="loading" class="spinner"></span>
                      Add to Team
                    </button>
          </form>
        </div>
              </div>

              <!-- Meeting Scheduler -->
              <div class="card meeting-card">
                <div class="card-header">
                  <h3>
                    <span class="card-icon">📅</span>
                    Schedule Meeting
                  </h3>
                </div>
                <div class="card-content">
                  <form @submit.prevent="proposeLocal" class="form meeting-grid">
                    <div class="form-group">
                      <label for="meetDate">Date</label>
                      <input id="meetDate" type="date" v-model="meetDate" class="form-input" required />
                    </div>
                    <div class="form-group">
                      <label for="meetTime">Time</label>
                      <input id="meetTime" type="time" v-model="meetTime" class="form-input" required />
                    </div>
                    <div class="form-group">
                      <label for="meetTz">Timezone</label>
                      <input v-if="timezones.length" v-model.trim="tzSearchMeet" class="form-input tz-search" placeholder="Search city/timezone" />
                      <select id="meetTz" v-model="meetTz" class="form-input" required>
                        <option v-for="tz in tzOptionsMeet" :key="tz" :value="tz">{{ tz }}</option>
                      </select>
                    </div>
                    <div class="form-group" style="align-self:end">
                      <button type="submit" class="btn btn-primary" :disabled="loading">
                        <span v-if="loading" class="spinner"></span>
                        Compute Local Times
                      </button>
                    </div>
          </form>

                  <div v-if="schedule.length" class="schedule-results wide">
                    <h4>Meeting Schedule</h4>
                    <div class="utc-time">
                      <strong>UTC Time:</strong> {{ utcEcho }}
                    </div>
                    <div class="schedule-table">
            <table>
                        <thead>
                          <tr>
                            <th>Name</th>
                            <th>Timezone</th>
                            <th>Local Time</th>
                            <th>Day</th>
                          </tr>
                        </thead>
              <tbody>
                <tr v-for="row in schedule" :key="row.name">
                            <td class="member-name">{{ row.name }}</td>
                            <td class="timezone">{{ row.timezone }}</td>
                            <td class="local-time" :class="{ error: row.error }">
                              {{ row.local_datetime || row.error }}
                            </td>
                            <td class="weekday">{{ row.weekday }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  </main>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>

    <!-- Error Toast -->
    <div v-if="error" class="toast error" @click="error = ''">
      <span class="toast-icon">⚠️</span>
      <span class="toast-message">{{ error }}</span>
      <button class="toast-close">×</button>
    </div>

    <!-- Success Toast -->
    <div v-if="success" class="toast success" @click="success = ''">
      <span class="toast-icon">✅</span>
      <span class="toast-message">{{ success }}</span>
      <button class="toast-close">×</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue'

// State management
const loading = ref(false)
const error = ref('')
const success = ref('')

// URL state
const params = new URLSearchParams(window.location.search)
const team = ref(params.get('team'))
const authed = ref(false)
const showMe = ref(false)

// Home state
const memberName = ref('')
const memberTz = ref('')
const members = ref([])
const teamName = ref('')
const creatorName = ref('')
const creatorTz = ref('')
const teams = ref([])
const timezones = ref([])

// Team state
const requester = ref('')
const teamMembers = ref([])
const newTeamMember = ref('')
const utc = ref('')
const utcEcho = ref('')
const schedule = ref([])

// Personal state
const meName = ref('')
const meNameInput = ref('')
const meTimezone = ref('')
const meAvailability = ref(Array.from({ length: 24 }, (_, i) => (i >= 9 && i < 17 ? 1 : 0)))
const empty24 = ref(Array.from({ length: 24 }, () => 0))

// New state for display timezone and meeting scheduler
const displayTimezone = ref('UTC')
const meetDate = ref('')
const meetTime = ref('')
const meetTz = ref('UTC')
const hourTooltip = ref({ visible: false, x: 0, y: 0, names: [], hour: 0 })
const meDisplayTimezone = ref('UTC')
let isDragging = ref(false)
let dragSetTo = ref(1)
let dragLast = ref(-1)

// TZ search and curated popular list
const tzSearchHome = ref('')
const tzSearchMe = ref('')
const tzSearchMeDisplay = ref('')
const tzSearchDisplay = ref('')
const tzSearchMeet = ref('')
const popularTimezones = [
  'UTC', 'Europe/London', 'Europe/Paris', 'Europe/Berlin', 'Europe/Madrid',
  'Europe/Moscow', 'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles',
  'America/Toronto', 'America/Mexico_City', 'America/Sao_Paulo',
  'Asia/Singapore', 'Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Tokyo', 'Asia/Seoul', 'Asia/Kolkata',
  'Australia/Sydney', 'Pacific/Auckland'
]

function filterTzs(search){
  const s = (search || '').toLowerCase()
  const curated = popularTimezones.filter(tz => tz.toLowerCase().includes(s))
  const others = (timezones.value || []).filter(tz => !popularTimezones.includes(tz) && tz.toLowerCase().includes(s))
  return [...curated, ...others]
}

const tzOptionsHome = computed(() => filterTzs(tzSearchHome.value))
const tzOptionsMe = computed(() => filterTzs(tzSearchMe.value))
const tzOptionsMeDisplay = computed(() => filterTzs(tzSearchMeDisplay.value))
const tzOptionsDisplay = computed(() => filterTzs(tzSearchDisplay.value))
const tzOptionsMeet = computed(() => filterTzs(tzSearchMeet.value))

// API helper with error handling
const API_BASE = (typeof __API_BASE__ !== 'undefined' && __API_BASE__) ? __API_BASE__ : ''

async function api(payload) {
  try {
    loading.value = true
    error.value = ''
    const res = await fetch(`${API_BASE || ''}/app`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    if (!res.ok || data.ok === false) {
      throw new Error(data.error || data.detail || 'Request failed')
    }
    return data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    loading.value = false
  }
}

// Navigation functions
function goHome() {
  team.value = null
  showMe.value = false
  authed.value = false
  requester.value = ''
  teamMembers.value = []
  newTeamMember.value = ''
  utc.value = ''
  utcEcho.value = ''
  schedule.value = []
  const url = new URL(window.location.href)
  url.searchParams.delete('team')
  window.history.pushState({}, '', url.toString())
  loadMembers()
  loadTeams()
}

function openTeam(teamName) {
  team.value = teamName
  showMe.value = false
  authed.value = false
  requester.value = ''
  teamMembers.value = []
  newTeamMember.value = ''
  utc.value = ''
  utcEcho.value = ''
  schedule.value = []
  const url = new URL(window.location.href)
  url.searchParams.set('team', teamName)
  window.history.pushState({}, '', url.toString())
}

function openMe() {
  showMe.value = true
  team.value = null
  const url = new URL(window.location.href)
  url.searchParams.delete('team')
  window.history.pushState({}, '', url.toString())
}

// Watch for URL changes
watch(() => window.location.search, () => {
  const newParams = new URLSearchParams(window.location.search)
  const newTeam = newParams.get('team')
  if (newTeam !== team.value) {
    if (newTeam) {
      openTeam(newTeam)
    } else if (!showMe.value) {
      goHome()
    }
  }
})

// Member management
async function addMember() {
  try {
  await api({ action: 'add_member', name: memberName.value, timezone: memberTz.value })
  memberName.value = ''
  memberTz.value = ''
    success.value = 'Member added successfully!'
  await loadMembers()
  } catch {}
}

async function loadMembers() {
  try {
  const data = await api({ action: 'list_members' })
  members.value = data.members || []
  } catch {}
}

// Team management
async function loadTeams() {
  try {
  const data = await api({ action: 'list_teams' })
  teams.value = data.teams || []
  } catch {}
}

async function createTeam() {
  try {
  await api({ action: 'create_team', name: teamName.value, creator_name: creatorName.value, creator_timezone: creatorTz.value })
  teamName.value = ''
  creatorName.value = ''
  creatorTz.value = ''
    success.value = 'Team created successfully!'
  await loadTeams()
  } catch {}
}

async function join() {
  try {
  await api({ action: 'join_team', team: team.value, member_name: requester.value })
  authed.value = true
    success.value = 'Successfully joined the team!'
  await loadTeamDetail()
  } catch {}
}

async function loadTeamDetail() {
  try {
  const data = await api({ action: 'get_team', team: team.value, requester_name: requester.value })
  teamMembers.value = data.members || []
  } catch {}
}

async function addToTeam() {
  try {
  await api({ action: 'add_member_to_team', team: team.value, member_name: newTeamMember.value })
  newTeamMember.value = ''
    success.value = 'Member added to team!'
  await loadTeamDetail()
  } catch {}
}

// Meeting scheduling
async function propose() {
  try {
  const data = await api({ action: 'propose_meeting', utc_datetime: utc.value })
  utcEcho.value = data.utc_datetime
  schedule.value = data.schedule || []
    success.value = 'Meeting schedule computed!'
  } catch {}
}

async function proposeLocal() {
  try {
    const data = await api({ action: 'propose_meeting_local', date: meetDate.value, time: meetTime.value, timezone: meetTz.value })
    utcEcho.value = data.utc_datetime
    schedule.value = data.schedule || []
    success.value = 'Meeting schedule computed!'
  } catch {}
}

// Timezones
async function loadTimezones() {
  try {
    const data = await api({ action: 'list_timezones' })
    timezones.value = data.timezones || []
  } catch {}
}

// Personal space
async function loadMe() {
  try {
    const name = meNameInput.value
    const data = await api({ action: 'get_member', name })
    meName.value = data.member.name
    meTimezone.value = data.member.timezone
    meAvailability.value = Array.isArray(data.member.availability) && data.member.availability.length === 24 ? data.member.availability.slice() : meAvailability.value
    success.value = 'Loaded your profile.'
  } catch (e) {
    error.value = 'Member not found. Make sure you added yourself on Home.'
  }
}

async function saveTimezone() {
  try {
    await api({ action: 'update_member_timezone', name: meName.value, timezone: meTimezone.value })
    success.value = 'Timezone updated.'
  } catch {}
}

function toggleHour(i) {
  meAvailability.value[i] = meAvailability.value[i] === 1 ? 0 : 1
}

async function saveAvailability() {
  try {
    await api({ action: 'update_availability', name: meName.value, availability: meAvailability.value })
    success.value = 'Availability saved.'
  } catch {}
}

// Aggregate availability for team
const aggregateCounts = computed(() => {
  const counts = Array.from({ length: 24 }, () => 0)
  for (const m of teamMembers.value || []) {
    const avail = m.availability || []
    for (let i = 0; i < 24; i++) {
      counts[i] += avail[i] ? 1 : 0
    }
  }
  return counts
})

function aggregateStyle(hour) {
  const max = Math.max(1, ...aggregateCounts.value)
  const ratio = aggregateCounts.value[hour] / max
  const bg = `linear-gradient(0deg, rgba(16,185,129,${Math.max(0.15, ratio)}) 0%, rgba(16,185,129,${Math.max(0.15, ratio)}) 100%)`
  return { background: bg }
}

// New computed property for display timezone label
const displayTzLabel = computed(() => {
  if (displayTimezone.value === 'UTC') return 'UTC'
  try {
    const now = new Date()
    const utc = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 0, 0, 0))
    const fmt = new Intl.DateTimeFormat('en-US', { hour: '2-digit', hour12: false, timeZone: displayTimezone.value })
    return fmt.format(utc) + ' (Local)'
  } catch { return displayTimezone.value }
})

// New function for hour label
function hourLabel(h){
  // Keep labels fixed as 00..23 so the axis is stable; data shifts per timezone
  const n = ((h % 24) + 24) % 24
  return String(n).padStart(2, '0')
}

// New computed property for team availability in display timezone
const teamAvailabilityLocal = computed(() => {
  // Accurate mapping: compute local hour for each UTC hour using Intl with timeZone
  const map = Array.from({ length: 24 }, () => [])
  const tz = displayTimezone.value || 'UTC'
  for (const m of teamMembers.value || []) {
    const avail = m.availability || []
    for (let h = 0; h < 24; h++) {
      if (avail[h]) {
        try {
          const d = new Date(Date.UTC(2000, 0, 1, h, 0, 0))
          const fmt = new Intl.DateTimeFormat('en-US', { hour: '2-digit', hour12: false, timeZone: tz })
          const localHour = parseInt(fmt.format(d), 10)
          map[localHour].push(m.name)
        } catch {
          map[h].push(m.name)
        }
      }
    }
  }
  return map
})

function aggregateStyleLocal(hour) {
  const names = teamAvailabilityLocal.value[hour] || []
  const max = Math.max(1, ...teamAvailabilityLocal.value.map(a => a.length))
  const ratio = names.length / max
  const bg = `linear-gradient(0deg, rgba(16,185,129,${Math.max(0.15, ratio)}) 0%, rgba(16,185,129,${Math.max(0.15, ratio)}) 100%)`
  return { background: bg }
}

function showHourTooltip(hour, evt){
  hourTooltip.value = { visible: true, x: evt.clientX, y: evt.clientY, names: teamAvailabilityLocal.value[hour] || [], hour }
}
function hideHourTooltip(){ hourTooltip.value.visible = false }
function toggleHourPopup(hour, evt){ showHourTooltip(hour, evt) }

// Map between UTC-stored availability and local display/editing for My Space
function utcToLocalHour(utcHour, tz){
  try {
    const d = new Date(Date.UTC(2000,0,1,utcHour,0,0))
    const fmt = new Intl.DateTimeFormat('en-US', { hour: '2-digit', hour12: false, timeZone: tz })
    return parseInt(fmt.format(d), 10)
  } catch { return utcHour }
}

function localToUtcHour(localHour, tz){
  // Find the UTC hour that maps to the given local hour
  for (let h = 0; h < 24; h++){
    if (utcToLocalHour(h, tz) === localHour) return h
  }
  return localHour
}

const meAvailabilityLocal = computed(() => {
  const arr = Array.from({ length: 24 }, () => 0)
  for (let h = 0; h < 24; h++){
    if (meAvailability.value[h]){
      const lh = utcToLocalHour(h, meDisplayTimezone.value || 'UTC')
      arr[lh] = 1
    }
  }
  return arr
})

function toggleMeHourLocal(localHour){
  const utcHour = localToUtcHour(localHour, meDisplayTimezone.value || 'UTC')
  meAvailability.value[utcHour] = meAvailability.value[utcHour] === 1 ? 0 : 1
}

function hourLabelMe(h){
  // Fixed labels 00..23 for editing grid; mapping handles timezone conversion
  const n = ((h % 24) + 24) % 24
  return String(n).padStart(2, '0')
}

// Default My Space display tz to user's timezone when loaded
watch(meTimezone, (tz) => {
  if (tz) meDisplayTimezone.value = tz
})

// Drag-to-select availability
function startDrag(isTouch = false, evt){
  isDragging.value = true
  const idx = indexFromEvent(evt, isTouch)
  if (idx != null){
    // modifiers: Alt to clear, Shift to fill
    if (evt && evt.altKey) dragSetTo.value = 0
    else if (evt && evt.shiftKey) dragSetTo.value = 1
    else dragSetTo.value = meAvailabilityLocal.value[idx] === 1 ? 0 : 1
    applyDragAt(idx)
  }
}

function onDrag(evt, isTouch = false){
  if (!isDragging.value) return
  const idx = indexFromEvent(evt, isTouch)
  if (idx != null && idx !== dragLast.value){
    applyDragAt(idx)
  }
}

function endDrag(){
  isDragging.value = false
  dragLast.value = -1
}

function indexFromEvent(evt, isTouch){
  const target = (isTouch ? document.elementFromPoint(evt.touches[0].clientX, evt.touches[0].clientY) : evt.target)
  if (!target) return null
  const el = target.closest && target.closest('.hour')
  if (!el) return null
  const idx = parseInt(el.getAttribute('data-index'))
  return isNaN(idx) ? null : idx
}

function applyDragAt(localIdx){
  dragLast.value = localIdx
  const utcHour = localToUtcHour(localIdx, meDisplayTimezone.value || 'UTC')
  meAvailability.value[utcHour] = dragSetTo.value
}

// Auto-hide success messages
watch(success, (val) => { if (val) setTimeout(() => { success.value = '' }, 3000) })

// Initialize app
onMounted(() => {
  if (!team.value) {
    loadMembers()
    loadTeams()
  }
  loadTimezones()
})
</script>

<style>
/* CSS Variables for theming */
:root {
  --primary-color: #3b82f6;
  --primary-hover: #2563eb;
  --secondary-color: #6b7280;
  --success-color: #10b981;
  --error-color: #ef4444;
  --warning-color: #f59e0b;
  
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #f1f5f9;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  
  --border-color: #e2e8f0;
  --border-hover: #cbd5e1;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --text-primary: #f1f5f9;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    
    --border-color: #334155;
    --border-hover: #475569;
  }
}

/* Reset and base styles */
* {
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  margin: 0;
  padding: 0;
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  line-height: 1.6;
  font-size: 16px;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header */
.header {
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg) 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.logo-icon {
  font-size: 1.75rem;
}

.nav {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background: none;
  border: none;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-link.active {
  background: var(--primary-color);
  color: white;
}

.nav-separator {
  color: var(--text-muted);
  font-weight: 500;
}

.nav-current {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--text-primary);
  font-weight: 600;
}

.nav-icon {
  font-size: 1rem;
}

/* Main content */
.main {
  flex: 1;
  padding: var(--spacing-2xl) 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

/* Welcome section */
.welcome-section {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.welcome-section h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 var(--spacing-md) 0;
  background: linear-gradient(135deg, var(--primary-color), var(--success-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.welcome-section p {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin: 0;
  max-width: 600px;
  margin: 0 auto;
}

/* Grid layout */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-2xl);
}

/* Cards */
.card {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--border-hover);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-tertiary);
}

.card-header h3 {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
}

.card-icon {
  font-size: 1.25rem;
}

.badge {
  background: var(--primary-color);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  min-width: 1.5rem;
  text-align: center;
}

.card-content {
  padding: var(--spacing-lg);
}

/* Forms */
.form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-input {
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  background: var(--bg-primary);
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1);
}

.form-input::placeholder {
  color: var(--text-muted);
}

.form-help {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: var(--spacing-xs);
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--border-color);
}

.btn-sm {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: 0.75rem;
}

.btn-icon {
  font-size: 1rem;
}

/* Spinner */
.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Lists */
.members-list,
.teams-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.member-item,
.team-item {
  padding: var(--spacing-md);
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;
}

.team-item {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.team-item:hover {
  background: var(--border-color);
  transform: translateX(4px);
}

.member-info,
.team-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.member-name,
.team-name {
  font-weight: 500;
  color: var(--text-primary);
}

.member-timezone,
.team-count {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.team-arrow {
  color: var(--text-muted);
  font-size: 1.25rem;
  transition: transform 0.2s ease;
}

.team-item:hover .team-arrow {
  transform: translateX(4px);
}

/* Empty states */
.empty-state {
  text-align: center;
  padding: var(--spacing-2xl) var(--spacing-lg);
  color: var(--text-muted);
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: var(--spacing-md);
}

.empty-state p {
  margin: 0;
  font-size: 0.875rem;
}

/* Team view */
.team-view {
  max-width: 1000px;
  margin: 0 auto;
}

.team-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.team-header h2 {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 var(--spacing-sm) 0;
}

.team-icon {
  font-size: 1.5rem;
}

.team-header p {
  color: var(--text-secondary);
  margin: 0;
}

.auth-card {
  max-width: 400px;
  margin: 0 auto var(--spacing-2xl) auto;
}

/* Meeting schedule */
.schedule-results {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--border-color);
}

.schedule-results h4 {
  margin: 0 0 var(--spacing-md) 0;
  font-size: 1.125rem;
  font-weight: 600;
}

.utc-time {
  background: var(--bg-tertiary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-lg);
  font-size: 0.875rem;
}

.schedule-table {
  overflow-x: auto;
}

.schedule-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.schedule-table th,
.schedule-table td {
  padding: var(--spacing-md);
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.schedule-table th {
  background: var(--bg-tertiary);
  font-weight: 600;
  color: var(--text-primary);
}

.schedule-table td {
  color: var(--text-secondary);
}

.schedule-table .member-name {
  font-weight: 500;
  color: var(--text-primary);
}

.schedule-table .local-time.error {
  color: var(--error-color);
  font-style: italic;
}

/* Loading overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Toasts */
.toast {
  position: fixed;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  z-index: 1001;
  cursor: pointer;
  max-width: 400px;
  animation: slideIn 0.3s ease;
}

.toast.error {
  background: var(--error-color);
  color: white;
}

.toast.success {
  background: var(--success-color);
  color: white;
}

.toast-icon {
  font-size: 1.25rem;
}

.toast-message {
  flex: 1;
  font-size: 0.875rem;
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: background 0.2s ease;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .container {
    padding: 0 var(--spacing-md);
  }
  
  .header-content {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }
  
  .nav {
    justify-content: center;
  }
  
  .welcome-section h2 {
    font-size: 2rem;
  }
  
  .grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }
  
  .card-header {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: flex-start;
  }
  
  .schedule-table {
    font-size: 0.75rem;
  }
  
  .schedule-table th,
  .schedule-table td {
    padding: var(--spacing-sm);
  }
  
  .toast {
    right: var(--spacing-md);
    left: var(--spacing-md);
    max-width: none;
  }
}

@media (max-width: 480px) {
  .main {
    padding: var(--spacing-lg) 0;
  }
  
  .welcome-section h2 {
    font-size: 1.75rem;
  }
  
  .card-content {
    padding: var(--spacing-md);
  }
  
  .btn {
    padding: var(--spacing-sm) var(--spacing-md);
  }
}

.availability-bar { display: grid; grid-template-columns: repeat(24, 1fr); gap: 2px; margin-top: 8px; }
.availability-bar .cell { height: 10px; background: var(--bg-tertiary); border-radius: 2px; }
.availability-bar .cell.on { background: var(--success-color); }

.availability-aggregate { display: grid; grid-template-columns: repeat(24, 1fr); gap: 4px; }
.aggregate-hour { height: 24px; border: 1px solid var(--border-color); border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; color: var(--text-secondary); background: var(--bg-tertiary); }

.availability-editor { display: grid; grid-template-columns: repeat(12, 1fr); gap: 6px; }
.availability-editor .hour { padding: 8px 0; border: 1px solid var(--border-color); border-radius: 6px; background: var(--bg-tertiary); color: var(--text-secondary); cursor: pointer; }
.availability-editor .hour.on { background: rgba(16, 185, 129, 0.25); color: var(--text-primary); border-color: var(--success-color); }

.me-view .card { overflow: visible; }
.tz-picker { display: flex; align-items: center; gap: 8px; }
.meeting-grid { display: grid; grid-template-columns: repeat(4, minmax(160px, 1fr)); gap: 16px; }
.schedule-results.wide { margin-top: 24px; }
.hour-tooltip { position: fixed; background: var(--bg-primary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: 6px; padding: 8px 10px; box-shadow: var(--shadow-lg); font-size: 12px; z-index: 1100; max-width: 260px; }
.tz-search { margin-bottom: 6px; }
</style>


