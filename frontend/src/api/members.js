// Members API calls - create, read, update, delete members
import { apiRequest } from './index.js'
import { fetchMembersMock, updateMemberMock, updateAvailabilityMock } from './members.mock.js'

const USE_MOCK_API = import.meta.env.VITE_USE_MOCKS === 'true'

// Members API functions
export const membersAPI = {
  // Get all members
  async getAllMembers() {
    try {
      if (USE_MOCK_API) {
        return await fetchMembersMock()
      }
      const response = await apiRequest('/members')
      return response
    } catch (error) {
      console.error('Get members failed:', error)
      throw error
    }
  },

  // Get member by ID
  async getMemberById(id) {
    try {
      const response = await apiRequest(`/members/${id}`)
      return response
    } catch (error) {
      console.error('Get member failed:', error)
      throw error
    }
  },

  // Create new member
  async createMember(memberData) {
    try {
      const response = await apiRequest('/members', {
        method: 'POST',
        body: JSON.stringify(memberData),
      })
      return response
    } catch (error) {
      console.error('Create member failed:', error)
      throw error
    }
  },

  // Update member
  async updateMember(id, memberData) {
    try {
      if (USE_MOCK_API) {
        return await updateMemberMock(id, memberData)
      }
      const response = await apiRequest(`/members/${id}`, {
        method: 'PUT',
        body: JSON.stringify(memberData),
      })
      return response
    } catch (error) {
      console.error('Update member failed:', error)
      throw error
    }
  },

  // Delete member
  async deleteMember(id) {
    try {
      const response = await apiRequest(`/members/${id}`, {
        method: 'DELETE',
      })
      return response
    } catch (error) {
      console.error('Delete member failed:', error)
      throw error
    }
  },

  // Update member availability
  async updateAvailability(id, availability) {
    try {
      if (USE_MOCK_API) {
        return await updateAvailabilityMock(id, availability)
      }
      const response = await apiRequest(`/members/${id}/availability`, {
        method: 'PUT',
        body: JSON.stringify({ availability }),
      })
      return response
    } catch (error) {
      console.error('Update availability failed:', error)
      throw error
    }
  },

  // Get member availability
  async getAvailability(id) {
    try {
      const response = await apiRequest(`/members/${id}/availability`)
      return response
    } catch (error) {
      console.error('Get availability failed:', error)
      throw error
    }
  },

  // Get members by team
  async getMembersByTeam(teamId) {
    try {
      const response = await apiRequest(`/teams/${teamId}/members`)
      return response
    } catch (error) {
      console.error('Get team members failed:', error)
      throw error
    }
  }
}

export default membersAPI

// Named exports for store compatibility
export async function fetchMembers() {
  return membersAPI.getAllMembers()
}

export async function updateMember(id, memberData) {
  return membersAPI.updateMember(id, memberData)
}

export async function updateAvailability(id, availability) {
  return membersAPI.updateAvailability(id, availability)
}