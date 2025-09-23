import { defineStore } from 'pinia'
import { teamsAPI } from '../../api/teams.js'
import { meetingsAPI } from '../../api/meetings.js'

export const useTeamsStore = defineStore('teams', {
  state: () => ({
    teams: [],
    currentTeam: null,
    loading: false,
    error: null
  }),

  getters: {
    allTeams: (state) => state.teams,
    getTeamById: (state) => (id) => state.teams.find(team => team.id === id),
    isLoading: (state) => state.loading,
    hasError: (state) => !!state.error
  },

  actions: {
    async fetchTeams() {
      this.loading = true
      this.error = null
      
      try {
        const teams = await teamsAPI.getAllTeams()
        this.teams = Array.isArray(teams) ? teams : []
      } catch (error) {
        this.error = error.message
        console.error('Error fetching teams:', error)
      } finally {
        this.loading = false
      }
    },

    async addMember(teamId, memberId) {
      this.loading = true
      this.error = null
      try {
        const updated = await teamsAPI.addMemberToTeam(teamId, memberId)
        const idx = this.teams.findIndex(t => t.id === teamId)
        if (idx !== -1) {
          this.teams[idx] = updated
          if (this.currentTeam && this.currentTeam.id === teamId) this.currentTeam = updated
        }
        return updated
      } catch (error) {
        this.error = error.message
        console.error('Error adding member:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createTeam(teamData) {
      this.loading = true
      this.error = null
      
      try {
        const newTeam = await teamsAPI.createTeam(teamData)
        this.teams = [...this.teams, newTeam]
        return newTeam
      } catch (error) {
        this.error = error.message
        console.error('Error creating team:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateTeam(teamId, updates) {
      this.loading = true
      this.error = null
      
      try {
        const updated = await teamsAPI.updateTeam(teamId, updates)
        const teamIndex = this.teams.findIndex(team => team.id === teamId)
        if (teamIndex !== -1) this.teams[teamIndex] = updated
      } catch (error) {
        this.error = error.message
        console.error('Error updating team:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteTeam(teamId) {
      this.loading = true
      this.error = null
      
      try {
        await teamsAPI.deleteTeam(teamId)
        this.teams = this.teams.filter(team => team.id !== teamId)
      } catch (error) {
        this.error = error.message
        console.error('Error deleting team:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    setCurrentTeam(team) {
      this.currentTeam = team
    },

    async fetchTeam(teamId) {
      this.loading = true
      this.error = null
      
      try {
        const team = await teamsAPI.getTeamById(teamId)
        if (team) this.currentTeam = team
      } catch (error) {
        this.error = error.message
        console.error('Error fetching team:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchTeamAvailability(teamId) {
      this.loading = true
      this.error = null
      
      try {
        console.log('Fetching team availability for team:', teamId)
      } catch (error) {
        this.error = error.message
        console.error('Error fetching team availability:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchTeamMembers(teamId) {
      this.loading = true
      this.error = null
      
      try {
        const members = await teamsAPI.getTeamMembers(teamId)
        return members
      } catch (error) {
        this.error = error.message
        console.error('Error fetching team members:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchTeamMeetings(teamId) {
      this.loading = true
      this.error = null
      
      try {
        const meetings = await meetingsAPI.getMeetingsByTeam(teamId)
        return meetings
      } catch (error) {
        this.error = error.message
        console.error('Error fetching team meetings:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})