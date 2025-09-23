// Meetings API calls - create, read, update, delete meetings and votes
import { apiRequest } from './index.js'
import { fetchMeetingsMock, getMeetingByIdMock, createMeetingMock, updateMeetingMock, deleteMeetingMock, fetchMeetingMembersMock, fetchMeetingVotesMock, submitVoteMock, fetchVoteResultsMock } from './meetings.mock.js'

const USE_MOCK_API = import.meta.env.VITE_USE_MOCKS === 'true'

export const meetingsAPI = {
  async getAllMeetings() {
    try {
      if (USE_MOCK_API) return await fetchMeetingsMock()
      return await apiRequest('/meetings')
    } catch (error) {
      console.error('Get meetings failed:', error)
      throw error
    }
  },

  async getMeetingsByTeam(teamId) {
    try {
      if (USE_MOCK_API) {
        const all = await fetchMeetingsMock()
        return (all || []).filter(m => m.teamId === teamId)
      }
      return await apiRequest(`/teams/${teamId}/meetings`)
    } catch (error) {
      console.error('Get team meetings failed:', error)
      throw error
    }
  },

  async getMeetingById(id) {
    try {
      if (USE_MOCK_API) return await getMeetingByIdMock(id)
      return await apiRequest(`/meetings/${id}`)
    } catch (error) {
      console.error('Get meeting failed:', error)
      throw error
    }
  },

  async createMeeting(teamId, meetingData) {
    try {
      const payload = {
        ...meetingData,
        ...(meetingData?.timezone ? { timezone: meetingData.timezone } : {})
      }
      if (USE_MOCK_API) return await createMeetingMock(teamId, payload)
      return await apiRequest(`/teams/${teamId}/meetings`, {
        method: 'POST',
        body: JSON.stringify(payload),
      })
    } catch (error) {
      console.error('Create meeting failed:', error)
      throw error
    }
  },

  async updateMeeting(id, meetingData) {
    try {
      const payload = {
        ...meetingData,
        ...(meetingData?.timezone ? { timezone: meetingData.timezone } : {})
      }
      if (USE_MOCK_API) return await updateMeetingMock(id, payload)
      return await apiRequest(`/meetings/${id}`, {
        method: 'PUT',
        body: JSON.stringify(payload),
      })
    } catch (error) {
      console.error('Update meeting failed:', error)
      throw error
    }
  },

  async deleteMeeting(id) {
    try {
      if (USE_MOCK_API) return await deleteMeetingMock(id)
      return await apiRequest(`/meetings/${id}`, { method: 'DELETE' })
    } catch (error) {
      console.error('Delete meeting failed:', error)
      throw error
    }
  },

  async getMeetingMembers(meetingId) {
    try {
      if (USE_MOCK_API) return await fetchMeetingMembersMock(meetingId)
      return await apiRequest(`/meetings/${meetingId}/members`)
    } catch (error) {
      console.error('Get meeting members failed:', error)
      throw error
    }
  },

  async getMeetingVotes(meetingId) {
    try {
      if (USE_MOCK_API) return await fetchMeetingVotesMock(meetingId)
      return await apiRequest(`/meetings/${meetingId}/votes`)
    } catch (error) {
      console.error('Get meeting votes failed:', error)
      throw error
    }
  },

  async submitVote(meetingId, voteData) {
    try {
      if (USE_MOCK_API) return await submitVoteMock(meetingId, voteData)
      return await apiRequest(`/meetings/${meetingId}/votes`, {
        method: 'POST',
        body: JSON.stringify(voteData),
      })
    } catch (error) {
      console.error('Submit vote failed:', error)
      throw error
    }
  },

  async getVoteResults(meetingId) {
    try {
      if (USE_MOCK_API) return await fetchVoteResultsMock(meetingId)
      return await apiRequest(`/meetings/${meetingId}/results`)
    } catch (error) {
      console.error('Get vote results failed:', error)
      throw error
    }
  }
}

export default meetingsAPI


