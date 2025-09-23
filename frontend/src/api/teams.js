// Teams API calls - create, read, update, delete teams
import { apiRequest } from './index.js'
import { fetchTeamsMock, getTeamByIdMock, createTeamMock, updateTeamMock, deleteTeamMock, getTeamMembersMock } from './teams.mock.js'
import { fetchMeetingsMock, createMeetingMock } from './meetings.mock.js'

const USE_MOCK_API = import.meta.env.VITE_USE_MOCKS === 'true'

// Removed timezone normalization; expect callers/mocks to provide IANA IDs

// Teams API functions
export const teamsAPI = {
  // Get all teams
  async getAllTeams() {
    try {
      if (USE_MOCK_API) {
        return await fetchTeamsMock()
      }
      const response = await apiRequest('/teams')
      return response
    } catch (error) {
      console.error('Get teams failed:', error)
      throw error
    }
  },

  // Get team by ID
  async getTeamById(id) {
    try {
      if (USE_MOCK_API) {
        return await getTeamByIdMock(id)
      }
      const response = await apiRequest(`/teams/${id}`)
      return response
    } catch (error) {
      console.error('Get team failed:', error)
      throw error
    }
  },

  // Create new team
  async createTeam(teamData) {
    try {
      const payload = { ...teamData }
      if (USE_MOCK_API) {
        return await createTeamMock(payload)
      }
      const response = await apiRequest('/teams', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      return response
    } catch (error) {
      console.error('Create team failed:', error)
      throw error
    }
  },

  // Update team
  async updateTeam(id, teamData) {
    try {
      const payload = { ...teamData }
      if (USE_MOCK_API) {
        return await updateTeamMock(id, payload)
      }
      const response = await apiRequest(`/teams/${id}`, {
        method: 'PUT',
        body: JSON.stringify(payload),
      })
      return response
    } catch (error) {
      console.error('Update team failed:', error)
      throw error
    }
  },

  // Delete team
  async deleteTeam(id) {
    try {
      if (USE_MOCK_API) {
        return await deleteTeamMock(id)
      }
      const response = await apiRequest(`/teams/${id}`, {
        method: 'DELETE',
      })
      return response
    } catch (error) {
      console.error('Delete team failed:', error)
      throw error
    }
  },

  // Add member to team
  async addMemberToTeam(teamId, memberId) {
    try {
      const response = await apiRequest(`/teams/${teamId}/members`, {
        method: 'POST',
        body: JSON.stringify({ memberId }),
      })
      return response
    } catch (error) {
      console.error('Add member to team failed:', error)
      throw error
    }
  },

  // Remove member from team
  async removeMemberFromTeam(teamId, memberId) {
    try {
      const response = await apiRequest(`/teams/${teamId}/members/${memberId}`, {
        method: 'DELETE',
      })
      return response
    } catch (error) {
      console.error('Remove member from team failed:', error)
      throw error
    }
  },

  // Get team members
  async getTeamMembers(teamId) {
    try {
      if (USE_MOCK_API) {
        return await getTeamMembersMock(teamId)
      }
      const response = await apiRequest(`/teams/${teamId}/members`)
      return response
    } catch (error) {
      console.error('Get team members failed:', error)
      throw error
    }
  },

  // Create meeting for team
  async createMeeting(teamId, meetingData) {
    try {
      if (USE_MOCK_API) return await createMeetingMock(teamId, meetingData)
      const response = await apiRequest(`/teams/${teamId}/meetings`, {
        method: 'POST',
        body: JSON.stringify(meetingData),
      })
      return response
    } catch (error) {
      console.error('Create meeting failed:', error)
      throw error
    }
  },

  // Get team meetings
  async getTeamMeetings(teamId) {
    try {
      if (USE_MOCK_API) {
        const all = await fetchMeetingsMock()
        return (all || []).filter(m => m.teamId === teamId)
      }
      const response = await apiRequest(`/teams/${teamId}/meetings`)
      return response
    } catch (error) {
      console.error('Get team meetings failed:', error)
      throw error
    }
  }
}

export default teamsAPI
