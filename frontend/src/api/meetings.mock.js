// src/api/meetings.mock.js
// Mock data and helpers for Meetings API

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export let MOCK_MEETINGS = [
  {
    id: '1',
    title: 'Weekly Standup',
    description: 'Weekly team standup meeting for development team',
    teamId: '1',
    creatorId: '1',
    scheduledTime: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
    votingStart: new Date().toISOString(),
    votingEnd: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'scheduled',
    createdAt: new Date().toISOString()
  },
  {
    id: '2',
    title: 'Project Review',
    description: 'Monthly project review meeting for development team',
    teamId: '1',
    creatorId: '1',
    scheduledTime: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    votingStart: new Date().toISOString(),
    votingEnd: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'voting',
    createdAt: new Date().toISOString()
  },
  {
    id: '3',
    title: 'Design Review',
    description: 'Weekly design review for design team',
    teamId: '2',
    creatorId: '2',
    scheduledTime: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
    votingStart: new Date().toISOString(),
    votingEnd: new Date(Date.now() + 10 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'scheduled',
    createdAt: new Date().toISOString()
  },
  {
    id: '4',
    title: 'Marketing Strategy',
    description: 'Monthly marketing strategy meeting',
    teamId: '3',
    creatorId: '1',
    scheduledTime: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString(),
    votingStart: new Date().toISOString(),
    votingEnd: new Date(Date.now() + 12 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'voting',
    createdAt: new Date().toISOString()
  }
]

export async function fetchMeetingsMock() {
  await delay(200)
  return MOCK_MEETINGS
}

export async function getMeetingByIdMock(meetingId) {
  await delay(120)
  return MOCK_MEETINGS.find(m => m.id === meetingId) || null
}

export async function createMeetingMock(teamId, meetingData) {
  await delay(150)
  // Derive creatorId from provided data or current mock-auth user in localStorage
  let derivedCreatorId = meetingData?.creatorId
  if (!derivedCreatorId && typeof localStorage !== 'undefined') {
    try {
      const stored = localStorage.getItem('user')
      if (stored) {
        const parsed = JSON.parse(stored)
        if (parsed && parsed.id) derivedCreatorId = parsed.id
      }
    } catch (_) {}
  }
  const newMeeting = {
    id: Date.now().toString(),
    teamId,
    status: meetingData?.status || 'voting',
    createdAt: new Date().toISOString(),
    ...meetingData,
    creatorId: derivedCreatorId || meetingData?.creatorId || null,
    // Ensure options exist and scheduledTime is undefined while voting
    options: Array.isArray(meetingData?.options) ? meetingData.options : [],
    scheduledTime: meetingData?.scheduledTime
  }
  MOCK_MEETINGS = [...MOCK_MEETINGS, newMeeting]
  return newMeeting
}

export async function updateMeetingMock(meetingId, updates) {
  await delay(150)
  const idx = MOCK_MEETINGS.findIndex(m => m.id === meetingId)
  if (idx === -1) throw new Error('Meeting not found')
  const updated = { ...MOCK_MEETINGS[idx], ...updates }
  MOCK_MEETINGS[idx] = updated
  return updated
}

export async function deleteMeetingMock(meetingId) {
  await delay(100)
  const before = MOCK_MEETINGS.length
  MOCK_MEETINGS = MOCK_MEETINGS.filter(m => m.id !== meetingId)
  return { deleted: before !== MOCK_MEETINGS.length }
}

export async function fetchMeetingMembersMock(meetingId) {
  await delay(120)
  // Minimal, could be enhanced to derive from teams/mock members later
  return [
    {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
      timezone: 'America/New_York',
      availability: {}
    },
    {
      id: '2',
      name: 'Jane Smith',
      email: 'jane@example.com',
      timezone: 'Asia/Singapore',
      availability: {}
    }
  ]
}

export async function fetchMeetingVotesMock(meetingId) {
  await delay(120)
  // Load from storage on each fetch to ensure persistence across sessions
  const stored = (typeof localStorage !== 'undefined' && localStorage.getItem('MOCK_VOTES'))
    ? JSON.parse(localStorage.getItem('MOCK_VOTES'))
    : MOCK_VOTES
  return (stored || []).filter(v => v.meetingId === meetingId)
}

export let MOCK_VOTES = (typeof localStorage !== 'undefined' && localStorage.getItem('MOCK_VOTES'))
  ? JSON.parse(localStorage.getItem('MOCK_VOTES'))
  : []

export async function submitVoteMock(meetingId, voteData) {
  await delay(120)
  const vote = {
    id: Date.now().toString(),
    meetingId,
    userId: voteData?.userId || 'current-user',
    timeSlot: voteData?.timeSlot,
    preference: voteData?.preference || 'high',
    createdAt: new Date().toISOString()
  }
  // replace previous vote by same user for this meeting
  const current = (typeof localStorage !== 'undefined' && localStorage.getItem('MOCK_VOTES'))
    ? JSON.parse(localStorage.getItem('MOCK_VOTES'))
    : MOCK_VOTES
  const updated = (current || []).filter(v => !(v.meetingId === meetingId && v.userId === vote.userId))
  updated.push(vote)
  MOCK_VOTES = updated
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('MOCK_VOTES', JSON.stringify(MOCK_VOTES))
  }
  return vote
}

export async function fetchVoteResultsMock(meetingId) {
  await delay(100)
  const votes = MOCK_VOTES.filter(v => v.meetingId === meetingId)
  const meeting = MOCK_MEETINGS.find(m => m.id === meetingId)
  const results = {}

  if (meeting && Array.isArray(meeting.options)) {
    meeting.options.forEach(opt => {
      results[opt.timeSlot] = { votes: 0, duration: opt.duration }
    })
  }

  votes.forEach(vote => {
    if (results[vote.timeSlot]) {
      results[vote.timeSlot].votes += 1
    }
  })

  return results
}


