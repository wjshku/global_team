// src/api/teams.mock.js
// Mock data and helpers for Teams API

import { MOCK_MEMBERS } from './members.mock.js'

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

// Seed teams based on data previously hardcoded in the teams store
export let MOCK_TEAMS = [
  {
    id: '1',
    name: 'Development Team',
    description: 'Main development team working on core features',
    timezone: 'Europe/Berlin',
    members: ['1', '2'],
    admin: '1',
    memberCount: 2,
    meetingCount: 3,
    createdAt: '2024-01-15T10:00:00Z'
  },
  {
    id: '2',
    name: 'Design Team',
    description: 'UI/UX design team creating beautiful interfaces',
    timezone: 'America/Los_Angeles',
    members: ['1', '2', '3'],
    admin: '2',
    memberCount: 2,
    meetingCount: 2,
    createdAt: '2024-01-16T14:30:00Z'
  },
  {
    id: '3',
    name: 'Marketing Team',
    description: 'Marketing and outreach team',
    timezone: 'America/New_York',
    members: ['3', '4'],
    admin: '3',
    memberCount: 2,
    meetingCount: 1,
    createdAt: '2024-01-17T09:15:00Z'
  }
]

export async function fetchTeamsMock() {
  await delay(200)
  return MOCK_TEAMS
}

export async function getTeamByIdMock(teamId) {
  await delay(120)
  return MOCK_TEAMS.find(t => t.id === teamId) || null
}

export async function createTeamMock(teamData) {
  await delay(150)
  const newTeam = {
    id: Date.now().toString(),
    memberCount: 0,
    meetingCount: 0,
    createdAt: new Date().toISOString(),
    members: Array.isArray(teamData?.members) ? teamData.members : [],
    admin: teamData?.admin || (Array.isArray(teamData?.members) ? teamData.members[0] : undefined) || null,
    ...teamData
  }
  MOCK_TEAMS = [...MOCK_TEAMS, newTeam]
  return newTeam
}

export async function updateTeamMock(teamId, updates) {
  await delay(150)
  const idx = MOCK_TEAMS.findIndex(t => t.id === teamId)
  if (idx === -1) throw new Error('Team not found')
  const updated = { ...MOCK_TEAMS[idx], ...updates }
  MOCK_TEAMS[idx] = updated
  return updated
}

export async function deleteTeamMock(teamId) {
  await delay(100)
  const before = MOCK_TEAMS.length
  MOCK_TEAMS = MOCK_TEAMS.filter(t => t.id !== teamId)
  return { deleted: before !== MOCK_TEAMS.length }
}

export async function getTeamMembersMock(teamId) {
  await delay(120)
  // Use member mock source of truth; filter by membership
  const members = MOCK_MEMBERS.filter(m => (m.teams || []).includes(teamId))
  return members
}

// Simple placeholder for team meetings list; the real data will live in meetings mock
export async function getTeamMeetingsMock(teamId, allMeetingsProvider) {
  await delay(120)
  const meetings = typeof allMeetingsProvider === 'function' ? allMeetingsProvider() : []
  return (meetings || []).filter(m => m.teamId === teamId)
}


